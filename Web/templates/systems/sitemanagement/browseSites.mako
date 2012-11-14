# -*- coding: utf-8 -*-
<%inherit file="/diracPage4.mako" />

<%def name="head_tags()">
${ h.javascript_link( "/javascripts/systems/sitemanagement/siteBrowser.js" ) }
</%def>


<%def name='body()'>
<script type="text/javascript">
  initGrid(${c.sitesData});
</script>
  
</%def>



