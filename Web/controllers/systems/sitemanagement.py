# -*- coding: utf-8 -*-

import logging
from dirac.lib.base import *
# import simplejson
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
    c.sitesData = self.fetchSites()['Value']
    return render("/systems/sitemanagement/browseSites.mako")

  # @jsonify
  def fetchSites(self):
    siteService = RPCClient('Framework/SiteManagement', timeout=300)
    sites = siteService.getSites()
    # sites = [{'status': 'ok', 'swver': '2012-11-02', 'name': 'LCG.KEK2.jp', 'history': '[["Active", "2012-08-02 18:45:21", "hideki", "Does not work"], ["Banned", "2012-08-02 16:55:15", "ricardo", "Does not work"], ["Active", "2012-08-02 16:20:55", "ricardo", "Does not work"], ["Banned", "2012-08-02 15:48:44", "ricardo", "Does not work"], ["Active", "2012-08-02 11:27:01", "ricardo", "Here we go again"], ["Banned", "2012-08-02 05:37:20", "ricardo", "until the GPFS issues are solved"], ["Active", "2012-07-20 11:47:41", "/C=JP/O=KEK/OU=CRC/CN=host/dirac.cc.kek.jp", "Lets try"]]'}, {'status': 'ok', 'swver': '2012-11-02', 'name': 'LCG.KIT.de', 'history': '[["Active", "2012-08-01 19:53:48", "ricardo", "try to add more resources"]]'}]
    return sites
