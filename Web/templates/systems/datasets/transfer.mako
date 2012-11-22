# -*- coding: utf-8 -*-
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<%inherit file="/diracPage.mako" />

<%def name="head_tags()">
${ h.javascript_link( "/javascripts/systems/datasets/datasetTransfer.js" ) }
<style>
.allPanel table.x-table-layout {
    width: 100%;
    height : 100%;
}

#action-panel .x-panel {
	margin-bottom:3px;
	margin-right:0;
}

</style>
</%def>

<%def name="body()">
<script type="text/javascript">
initDatasetTransfer();
</script>
</%def>
