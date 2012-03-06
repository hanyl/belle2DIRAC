# -*- coding: utf-8 -*-
import logging
import types
import simplejson
from dirac.lib.base import *
from dirac.lib.diset import getRPCClient, getTransferClient
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities import Time, List
from DIRAC.AccountingSystem.Client.ReportsClient import ReportsClient
from dirac.lib.webBase import defaultRedirect

log = logging.getLogger( __name__ )


class SitemanagementController( BaseController ):

  def index( self ):
    return defaultRedirect()

  def browse( self ):
    return render( "/systems/sitemanagement/browse.mako" )

