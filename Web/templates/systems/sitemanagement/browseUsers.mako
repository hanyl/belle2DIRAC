# -*- coding: utf-8 -*-
<%inherit file="/diracPage4.mako" />

<%def name="head_tags()">
${ h.javascript_link( "/javascripts/systems/sitemanagement/userBrowser.js" ) }
</%def>


<%def name='body()'>
<script type="text/javascript">
  initGrid(${c.usersData});
</script>
  
</%def>



