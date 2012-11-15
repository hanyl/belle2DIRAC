# -*- coding: utf-8 -*-

import logging
from dirac.lib.base import *
import simplejson
#from dirac.lib.diset import getRPCClient, getTransferClient
#from dirac.lib.credentials import authorizeAction
#from DIRAC import S_OK, S_ERROR, gLogger
#from DIRAC.Core.Utilities import Time, List
#from DIRAC.AccountingSystem.Client.ReportsClient import ReportsClient
from dirac.lib.webBase import defaultRedirect
from DIRAC.Core.DISET.RPCClient import RPCClient
from pylons import tmpl_context as c
from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin

log = logging.getLogger(__name__)


class SitemanagementController(BaseController):

  def index(self):
    return defaultRedirect()

  def browseUsers(self):
    diracAdmin = DiracAdmin()
    names = diracAdmin.csListUsers('belle')['Value']
    users = diracAdmin.csDescribeUsers(names)['Value']
    c.usersData = []
    for name in names:
      email = users[name]['Email']
      dn = users[name]['DN']
      c.usersData.append({'name': name, 'email': email, 'dn': dn})
    return render("/systems/sitemanagement/browseUsers.mako")

  def browseSites(self):
    c.sitesData = []
    # list banned sites
    diracAdmin = DiracAdmin()
    bannedSitesHandler = diracAdmin.getBannedSites(printOutput=False)
    if bannedSitesHandler['OK']:
      bannedNames = bannedSitesHandler['Value']
      history = [diracAdmin.getSiteMaskLogging(s)['Value'][s] for s in bannedNames][::-1]
      bannedSites = [{'name': s, 'status': 'banned',  'swver': '2012-01-01', 'history': simplejson.dumps(history)}]
    # list not banned sites
    wmsAdmin = RPCClient('WorkloadManagement/WMSAdministrator', timeout=120)
    siteMaskHandler = wmsAdmin.getSiteMask()
    if siteMaskHandler['OK']:
      notBannedNames = siteMaskHandler['Value']
    for siteName in notBannedNames:
      history = diracAdmin.getSiteMaskLogging(siteName)['Value'][siteName][::-1]
      c.sitesData.append({'name': siteName, 'status': 'ok', 'swver': '2012-11-02', 'history': simplejson.dumps(history)})
    # build list of all sites
    c.sitesData.extend(bannedSites)
    return render("/systems/sitemanagement/browseSites.mako")
