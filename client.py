from DIRAC.Core.DISET.RPCClient import RPCClient

siteService = RPCClient('Framework/SiteManagement', timeout=300)
# result = siteService.getMessage()
result = siteService.getSites()
# result = siteService.sendMessage('hiii')
# print result
if not result['OK']:
  print "Error while calling the service:", result['Message']
else:
  result['Value']
