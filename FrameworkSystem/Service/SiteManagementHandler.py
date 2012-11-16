########################################################################
# $HeadURL: $
########################################################################

"""
"""

__RCSID__ = "$Id: $"

from types import *
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.DISET.RPCClient import RPCClient
from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin
import simplejson

currentMessage = ""
messageAuthor = ""


def initializeSiteManagementHandler(serviceInfo):

  global currentMessage, messageAuthor
#  global currentMessage = "No Message"
  currentMessage = "No Message"
  messageAuthor = "No Author"
  return S_OK()


class SiteManagementHandler(RequestHandler):

  def initialize(self):
    """ Handler initialization
    """
    credDict = self.getRemoteCredentials()
    self.user = credDict['username']
    self.messageOfTheDay = self.getCSOption('MessageOfTheDay', 'NoMessageOfTheDay')

  types_getSites = []

  def export_getSites(self):
    """ Get a full list of sites from the service
    """
    activeSites = []
    bannedSites = []
    # list banned sites
    diracAdmin = DiracAdmin()
    bannedSitesHandler = diracAdmin.getBannedSites(printOutput=False)
    if bannedSitesHandler['OK']:
      bannedNames = bannedSitesHandler['Value']
      for bannedName in bannedNames:
        history = diracAdmin.getSiteMaskLogging(bannedName)['Value'][bannedName][::-1]
        bannedSites.append({'name': bannedName, 'status': 'banned',  'swver': '2012-01-01', 'history': simplejson.dumps(history)})
    # list not banned sites
    wmsAdmin = RPCClient('WorkloadManagement/WMSAdministrator', timeout=120)
    siteMaskHandler = wmsAdmin.getSiteMask()
    if siteMaskHandler['OK']:
      activeNames = siteMaskHandler['Value']
      for siteName in activeNames:
        history = diracAdmin.getSiteMaskLogging(siteName)['Value'][siteName][::-1]
        activeSites.append({'name': siteName, 'status': 'ok', 'swver': '2012-11-02', 'history': simplejson.dumps(history)})
    # build list of all sites
    sitesList = []
    sitesList.extend(activeSites)
    sitesList.extend(bannedSites)
    if not sitesList:
      return S_ERROR()
    return S_OK(sitesList)

  types_setMessage = [StringType]

  def export_setMessage(self, msg):
    """ Send a message to the service
    """
    global currentMessage, messageAuthor
    resultDict = {'Message': msg,
                  'Author': messageAuthor,
                  'MessageOfTheDay': self.messageOfTheDay}
    return S_OK(resultDict)
