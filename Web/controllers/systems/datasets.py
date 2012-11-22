# -*- coding: utf-8 -*-
import logging
import types
import simplejson
from AmgaClient import *
from dirac.lib.base import *
from dirac.lib.diset import getRPCClient, getTransferClient
import dirac.lib.credentials as credentials

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities import Time, List
from DIRAC.AccountingSystem.Client.ReportsClient import ReportsClient
from dirac.lib.webBase import defaultRedirect

log = logging.getLogger( __name__ )

class DatasetsController( BaseController ):

  LANG = "en"

  def index( self ):
    # Return a rendered template
    #   return render('/some/template.mako')
    # or, Return a response
    return defaultRedirect()

  def transfer( self ):
    return render( "/systems/datasets/transfer.mako" )

  def browse( self ):
    return render( "/systems/datasets/browse.mako" )

  @jsonify
  def getDatasetList( self ):
    callback = {}
    callback['datasets'] = []
    basePath = '/belle2/user/belle/' + credentials.getUsername() 
    try:
      amga = AmgaClient()
      dirs = amga.getSubdirectories(basePath, relative=True)
    except Exception, v:
      gLogger.error("section does not exist", "%s -> %s" % (sectionPath, str(v)))
    for dir in dirs:
      callback['datasets'].append({'dataset' : basePath+ '/'+dir })
    return callback

  @jsonify
  def getSiteList( self, dataset=None ):
    #XXX - remove sites with no SE
    callback = {}
    if dataset is None:
      #RPC = getRPCClient("ResourceStatus/ResourceStatus")
      RPC = getRPCClient("WorkloadManagement/JobMonitoring")
      #result = RPC.getSitesStatusList()
      result = RPC.getSites()
      print result
      gLogger.info("\033[0;31m LIST: \033[0m %s" % result)
      if result["OK"]:
        response = []
        if len(result["Value"])>0:
          sites = []
          result["Value"].remove("ANY")
          for site in result['Value']:
            sites.append({'sitename': site})
          callback['Value'] = sites
          return callback
        else:
          response = [["Nothing to display"]]
      else:
        response = [["Error during RPC call"]]
      return {"success":"true","result":response}
    else:
      pass
      


  @jsonify
  def expandSection( self ):
    try:
      parentNodeId = str( request.params[ 'node' ] )
      sectionPath = str( request.params[ 'nodePath' ] )
    except Exception, e:
      return S_ERROR( "Cannot expand section %s" % str( e ) )
    #cfgData = CFG()
    #cfgData.loadFromBuffer( session[ 'cfgData' ] )
    gLogger.info( "Expanding section", "%s" % sectionPath )
    try:
      amga = AmgaClient()
      dirs = amga.getSubdirectories(sectionPath, relative=True)
    except Exception, v:
      gLogger.error("section does not exist", "%s -> %s" % (sectionPath, str(v)))
      return S_ERROR("section does not exist", "%s -> %s" % (sectionPath, str(v)))
    #try:
    #  sectionCfg = cfgData
    #  for section in [ section for section in sectionPath.split( "/" ) if not section.strip() == "" ]:
    #    sectionCfg = sectionCfg[ section ]
    #except Exception, v:
    #  gLogger.error( "Section does not exist", "%s -> %s" % ( sectionPath, str( v ) ) )
    #  return S_ERROR( "Section %s does not exist: %s" % ( sectionPath, str( v ) ) )
    #gLogger.verbose( "Section to expand %s" % sectionPath )
    retData = []
    for entryName in dirs:
      entryName = entryName.lstrip('/')
      id = "%s/%s" % ( parentNodeId, entryName )
      comment = ""
      nodeDef = { 'text' : entryName, 'csName' : entryName, 'csComment' : comment }
    #  if not sectionCfg.isSection( entryName ):
    #     nodeDef[ 'leaf' ] = True
    #     nodeDef[ 'csValue' ] = sectionCfg[ entryName ]
    #  #Comment magic
    #  htmlC = self.__htmlComment( comment )
    #  if htmlC:
    #    qtipDict = { 'text' : htmlC }
    #    nodeDef[ 'qtipCfg' ] = qtipDict
      retData.append( nodeDef )
    return retData

