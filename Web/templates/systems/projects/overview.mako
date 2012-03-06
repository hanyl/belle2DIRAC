# -*- coding: utf-8 -*-
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<%inherit file="/diracPage.mako" />

<%def name="head_tags()">
${ h.javascript_link( "/javascripts/systems/projects/projectOverview.js" ) }
<style>
.allPanel table.x-table-layout {
    width: 100%;
    height : 100%;
}

#action-panel .x-panel {
	margin-bottom:3px;
	margin-right:0;
}

img.percentImage1 {
    background:          white url(/DIRAC/images/percentImage_back1.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage2 {
    background:          white url(/DIRAC/images/percentImage_back2.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage3 {
    background:          white url(/DIRAC/images/percentImage_back3.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage4 {
    background:          white url(/DIRAC/images/percentImage_back4.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage5 {
    background:          white url(/DIRAC/images/percentImage_back5.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}



img.percentImage1_small {
    background:          white url(/DIRAC/images/percentImage_back1_small.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage2_small {
    background:          white url(/DIRAC/images/percentImage_back2_small.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage3_small {
    background:          white url(/DIRAC/images/percentImage_back3_small.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage4_small {
    background:          white url(/DIRAC/images/percentImage_back4_small.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}

img.percentImage5_small {
    background:          white url(/DIRAC/images/percentImage_back5_small.png) top left no-repeat;
    padding:             0;
    margin:              5px 0 0 0;
    background-position: 1px 0;
}


.PercentageStatus1
{
  /* font-weight: bold; */
  color: #3eaf17;
/*  color: #68DC40;*/
}

.PercentageStatus2
{
  /* font-weight: bold; */
  color: #ded600;
}

.PercentageStatus3
{
  /* font-weight: bold; */
  color: #FFB005;
}

.PercentageStatus4
{
  /* font-weight: bold; */
  color: #FA3B00;
}

.PercentageStatus5
{
  /* font-weight: bold; */
  color: #808080;
}
</style>
</%def>

<%def name="body()">
<script type="text/javascript">
initProjectOverview();
</script>
</%def>
