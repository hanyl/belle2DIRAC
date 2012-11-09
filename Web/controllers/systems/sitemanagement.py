# -*- coding: utf-8 -*-
import logging
from dirac.lib.base import *
#from dirac.lib.diset import getRPCClient, getTransferClient
#from dirac.lib.credentials import authorizeAction
#from DIRAC import S_OK, S_ERROR, gLogger
#from DIRAC.Core.Utilities import Time, List
#from DIRAC.AccountingSystem.Client.ReportsClient import ReportsClient
from dirac.lib.webBase import defaultRedirect
from DIRAC.Core.DISET.RPCClient import RPCClient
from pylons import tmpl_context as c
from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin

log = logging.getLogger( __name__ )


class SitemanagementController( BaseController ):

  def index( self ):
    return defaultRedirect()

  def browse( self ):
    diracAdmin = DiracAdmin()
    names = diracAdmin.csListUsers( 'belle' )['Value']
    users = diracAdmin.csDescribeUsers(names)['Value']
    c.usersData = []
    for name in names:
      email = users[name]['Email']
      dn = users[name]['DN']
      c.usersData.append({ 'name': name, 'email': email, 'dn': dn })
    return render( "/systems/sitemanagement/browse.mako" )

  def browseSites( self ):
#    wmsAdmin = RPCClient( 'WorkloadManagement/WMSAdministrator', timeout = 120 )
#    result = wmsAdmin.getSiteMask()
#    c.lista = {"success":['1','444444']}
#    if result['OK']:
#      c.lista = {"success":['1','2','4','544']}
    return render( "/systems/sitemanagement/browse.mako" )