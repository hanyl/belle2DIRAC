# -*- coding: utf-8 -*-
import logging
import types
import simplejson
from datetime import tzinfo, timedelta, datetime
from dirac.lib.base import *
from dirac.lib.diset import getRPCClient, getTransferClient

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities import Time, List
from DIRAC.AccountingSystem.Client.ReportsClient import ReportsClient
from dirac.lib.webBase import defaultRedirect
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB

log = logging.getLogger( __name__ )

class ProjectsController( BaseController ):

  LANG = "en"

  def index( self ):
    # Return a rendered template
    #   return render('/some/template.mako')
    # or, Return a response
    return defaultRedirect()

  def overview( self ):
    return render( "/systems/projects/overview.mako" )

  @jsonify
  def getProjectsList( self ):
    try:
      start = int( request.params[ 'start' ] )
    except:
      start = 0
    try:
      limit = int( request.params[ 'limit' ] )
    except:
      limit = 0
    try:
      sortField = str( request.params[ 'sortField' ] ).replace( "_", "." )
      sortDir = str( request.params[ 'sortDirection' ] )
      sort = [ ( sortField, sortDir ) ]
    except:
      return S_ERROR( "Oops! Couldn't understand the request" )
    condDict = {}
    #This is our connection to the Job database
    rpcClient = getRPCClient( "WorkloadManagement/JobMonitoring" )
    lastMonth =  (datetime.today() - timedelta(365/12)).isoformat()
    result = rpcClient.getJobGroups(cutDate = lastMonth )
    #result = rpcClient.getJobGroups()
    if not result[ 'OK' ]:
      return result
    data = { 'numRecords' : len(result[ 'Value' ]), 'projects' : [] }
    for record in result['Value']:
      rD = {}
      counters = rpcClient.getCounters(['Status', 'Owner','OwnerGroup','LastUpdateTime','SubmissionTime'], {'JobGroup' : record})
      if not counters['OK']:
        return counters
      else:
        rD['LastUpdate'] = self.timeToNUnitAgo(self.mostRecentTime(counters['Value'], 'LastUpdateTime'))
        #rD['counters'] = counters['Value']
        rD['percentage'] = self.statusToPercentage(counters['Value'])
        rD['colours'] = self.statusToColours(counters['Value'])
	if rD['percentage'] == 1:
          if rD['colours'][0] > 0:
            rD['status'] = "Done - with failures"
          else:
            rD['status'] = "Done"
        else:
          rD['status'] = "Running"
      rD['SubmissionTime'] = str(self.mostRecentTime(counters['Value'],'SubmissionTime'))
      #cheat - get the first owner as they're all the same
      rD['Owner'] = counters["Value"][0][0]["Owner"]
      rD['OwnerGroup'] = counters["Value"][0][0]["OwnerGroup"]
      rD['proj_Name'] = record
      data['projects'].append( rD )
    print data
    return data

  def mostRecentTime(self, counters, timename="LastUpdateTime"):
    """
     Takes a bunch of data in DIRAC format (array of arrays of dicts) 
     and determines most recent time
    """
    utc = UTC()
    mostrecent = counters[0][0][timename].replace(tzinfo=utc)
    for entry in counters:
      if entry[0][timename].replace(tzinfo=utc) > mostrecent.replace(tzinfo=utc):
        mostrecent = entry[0][timename]
    return mostrecent
    


  def timeToNUnitAgo(self, time):
   """
    Takes a time (UTC) and converts it to a friendly string eg "N seconds ago"
   """
   utc = UTC()
   timediff = datetime.now().replace(tzinfo=utc) - time.replace(tzinfo=utc)
   return self.stringify_time(timediff) + " ago"

  def statusToPercentage(self, statuses):
    """
    Takes an aggregation of job statuses in the DIRAC format
    [[{"Status": "<status_name>"}, #], [{"Status": "<status_name>"}, #],...]
    and works out a reasonable percentage to display to a user for their project
    """
    terminal_states = ['Failed', 'Done']
    terminal = 0
    nonterminal = 0
    for status in statuses:
      if status[0]["Status"] in terminal_states:
        terminal = terminal + status[1]
      else:
        nonterminal = nonterminal + status[1]

    return terminal / (terminal + nonterminal)

  def statusToColours(self, statuses):
    """
    Takes an aggregation of job statuses in the DIRAC format
    [[{"Status": "<status_name>"}, #], [{"Status": "<status_name>"}, #],...]
    and attempts to divide the numbers into numbers for colours on a progress bar:
    R = bad
    G = good
    B = progress
    W = nothing!
    """
    red_states = ['Failed', 'Killed']
    green_states = ['Done', 'Completed']
    blue_states = ['Running']
    white_states = ['Submitted', 'Waiting', 'Matched','Checking']
    colours = [0,0,0,0] #RGB!
    for status in statuses:
      if status[0]["Status"] in red_states:
        colours[0] = colours[0] + status[1]
      elif status[0]["Status"] in green_states:
        colours[1] = colours[1] + status[1]
      elif status[0]["Status"] in blue_states:
        colours[2] = colours[2] + status[1]
      elif status[0]["Status"] in white_states:
        colours[3] = colours[3] + status[1]
      else:
        print "statusToColours(): Unknown status: %s", status
    print colours
    return colours

  #XXX - currently this just reschedules a single job
  # TODO = loop over all jobs in a jobGroup
  def __rescheduleProject(self,id):
    MANAGERRPC = getRPCClient("WorkloadManagement/JobManager")
    result = MANAGERRPC.rescheduleJob(id)
    if result["OK"]:
      c.result = ""
      c.result = {"success":"true","result":c.result}
    else:
      if result.has_key("InvalidJobIDs"):
        c.result = "Invalid JobIDs: %s" % result["InvalidJobIDs"]
        c.result = {"success":"false","error":c.result}
      elif result.has_key("NonauthorizedJobIDs"):
        c.result = "You are nonauthorized to delete jobs with JobID: %s" % result["NonauthorizedJobIDs"]
        c.result = {"success":"false","error":c.result}
      else:
        c.result = {"success":"false","error":result["Message"]}
    gLogger.info("RESET:",id)
    return c.result

####################################################################
# ActiveState Recipe 498062
# http://code.activestate.com/recipes/498062-nicely-readable-timedelta/
# Created by Björn Lindqvist on Sat, 2 Sep 2006 
####################################################################

# Singular and plural forms of time units in your language.
  unit_names = dict(sv = {"year" : ("år", "år"),
                        "month" : ("månad", "månader"),
                        "week" : ("vecka", "veckor"),
                        "day" : ("dag", "dagar"),
                        "hour" : ("timme", "timmar"),
                        "minute" : ("minut", "minuter"),
                        "second" : ("sekund", "sekunder")},
                  en = {"year" : ("year", "years"),
                        "month" : ("month", "months"),
                        "week" : ("week", "weeks"),
                        "day" : ("day", "days"),
                        "hour" : ("hour", "hours"),
                        "minute" : ("minute", "minutes"),
                        "second" : ("second", "seconds")})
                  
  num_repr = dict(sv = {1 : "en",
                      2 : "två",
                      3 : "tre",
                      4 : "fyra",
                      5 : "fem",
                      6 : "sex",
                      7 : "sju",
                      8 : "åtta",
                      9 : "nio",
                      10 : "tio",
                      11 : "elva",
                      12 : "tolv"},
                en = {1 : "one",
                      2 : "two",
                      3 : "three",
                      4 : "four",
                      5 : "five",
                      6 : "six",
                      7 : "seven",
                      8 : "eight",
                      9 : "nine",
                      10 : "ten",
                      11 : "eleven",
                      12 : "twelve"})

  def amount_to_str(self, amount, unit_name):
    # This is the Swedish hack. The Swedish language has two words for
    # "one" - "en" and "ett". Sometimes "en" is used and other times
    # "ett" is used. For the word "år," "ett" is used instead of "en."
    # No doubt other languages contain similar weirdness.
    if amount == 1 and unit_name == "year" and self.LANG == "sv":
        return "ett"
    if amount in self.num_repr[self.LANG]:
        return self.num_repr[self.LANG][amount]
    return str(amount)

  def seconds_in_units(self, seconds):
    """
    Returns a tuple containing the most appropriate unit for the
    number of seconds supplied and the value in that units form.

        >>> seconds_in_units(7700)
        (2, 'hour')
    """
    unit_limits = [("year", 365 * 24 * 3600),
                   ("month", 30 * 24 * 3600),
                   ("week", 7 * 24 * 3600),
                   ("day", 24 * 3600),
                   ("hour", 3600),
                   ("minute", 60)]
    for unit_name, limit in unit_limits:
        if seconds >= limit:
            amount = int(round(float(seconds) / limit))
            return amount, unit_name
    return seconds, "second"

  def stringify_time(self, td):
    """
    Converts a timedelta into a nicely readable string.

        >>> td = timedelta(days = 77, seconds = 5)
        >>> print readable_timedelta(td)
        two months
    """
    seconds = td.days * 3600 * 24 + td.seconds
    amount, unit_name = self.seconds_in_units(seconds)

    # Localize it.
    i18n_amount = self.amount_to_str(amount, unit_name)
    i18n_unit = self.unit_names[self.LANG][unit_name][1]
    if amount == 1:
        i18n_unit = self.unit_names[self.LANG][unit_name][0]
    return "%s %s" % (i18n_amount, i18n_unit)

#Stupid class for doing time manipulation
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

