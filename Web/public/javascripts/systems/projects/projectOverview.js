var gMainGrid = false;
var gContextMenu = false;

function initProjectOverview(){
  Ext.onReady(function(){
    renderPage();
  });
}

function initProjectList()
{
  var reader = new Ext.data.JsonReader({
          root : 'projects',
          totalProperty : 'numRecords',
          id : 'proj_Name',
          fields : [ "proj_Name", "colours", "status", "Owner", "OwnerGroup", "LastUpdate", "SubmissionTime"]
    });

  var store = new Ext.data.Store({
                reader: reader,
                url : "getProjectsList",
                autoLoad : true,
                sortInfo: { field: 'proj_Name', direction: 'DESC' },
                listeners : {
                        beforeload : cbStoreBeforeLoad
            }
        });





  var title = 'Project Summary';
  var columns = [
    {header:'',name:'checkBox',id:'checkBox',width:26,sortable:false,dataIndex:'JobIDcheckBox',renderer:renderSelect,hideable:false,fixed:true,menuDisabled:true},
    {header:'Project',sortable:true,dataIndex:'proj_Name',align:'left',hideable:false},
    {header:'',width:26,sortable:false,dataIndex:'StatusIcon',renderer:status,hideable:false,fixed:true,menuDisabled:true},
    {header:'Progress',width:160,sortable:true,dataIndex:'colours',align:'left',hideable:false,renderer:renderProgress},
    {header:'Status',sortable:true,dataIndex:'status',align:'left'},
    {header:'LastUpdate',sortable: true,dataIndex:'LastUpdate',sortable:false},
    //{header:'Submission Time',sortable:true,renderer:Ext.util.Format.dateRenderer('Y-m-d H:i:sP'),dataIndex:'SubmissionTime'},
    {header:'Submission Time',sortable:true,dataIndex:'SubmissionTime'},
    {header:'EventsperMin',sortable:true,dataIndex:'CPUTime',align:'left',hidden:true},
    {header:'JobType',sortable:true,dataIndex:'JobType',align:'left',hidden:true},
    {header:'Owner',sortable:true,dataIndex:'Owner',align:'left'},
    {header:'OwnerGroup',sortable:true,dataIndex:'OwnerGroup',align:'left',hidden:true}
  ];

  var tbar = [
              { handler:function(){ toggleAll(true) }, text:'Select all', width:150, tooltip:'Click to select all rows' },
              { handler:function(){ toggleAll(false) }, text:'Select none', width:150, tooltip:'Click to select all rows' },
              { handler:function(){ rescheduleProject() },   cls:"x-btn-text-icon", icon:gURLRoot+'/images/iface/reschedule.gif', text:'Reschedule Project', width:150, tooltip:'Click to Reschedule Project' },
              { handler:function(){ killProject() },   cls:"x-btn-text-icon", icon:gURLRoot+'/images/iface/close.gif', text:'Terminate Project', width:150, tooltip:'Click to Terminate Project' }
        ];

  var bbar = new Ext.PagingToolbar({
                                        pageSize: 50,
                                        store: store,
                                        displayInfo: true,
                                        displayMsg: 'Displaying entries {0} - {1} of {2}',
                                        emptyMsg: "No entries to display",
                                        items:[ '-',
                                                'Items per page: ', createNumItemsSelector(),
                                                '-']
        });


  gMainGrid = new Ext.grid.GridPanel( {store: store, columns: columns, region: 'center', tbar : tbar, bbar: bbar,  listeners : { sortchange : cbMainGridSortChange },
        } );


  if( title )
  	gMainGrid.setTitle( title );

  gContextMenu = new Ext.menu.Menu({
    id : 'OptionContextualMenu',
    items : [{ text : 'Show Jobs', listeners : { click : cbJump }
    },{ text : 'Show Failures', listeners : { click : cbJumpFailed }
    },
   ]
   })
  gMainGrid.on('cellcontextmenu', cbShowContextMenu );

  return gMainGrid;
}

function renderPage(store)
{
  gMainGrid = initProjectList();
  renderInMainViewport([gMainGrid]);
}

function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}



function cbStoreBeforeLoad( store, params )
{
        var sortState = store.getSortState()
        var bb = gMainGrid.getBottomToolbar();
        store.baseParams = { 'sortField' : sortState.field,
                                             'sortDirection' : sortState.direction,
                                                 'limit' : bb.pageSize,
                                           };
}

function cbShowContextMenu( grid, rowId, colId, event )
{
  event.stopEvent();
  gContextMenu.data = grid.getStore().getAt( rowId ).data;
  gContextMenu.project = (gContextMenu.data[ 'proj_Name' ]);
  gContextMenu.showAt(event.getXY());
}


function renderSelect( value, metadata, record, rowIndex, colIndex, store )
{
        return '<input id="' + record.id + '" type="checkbox"/>';
}

function renderProgress( value, metadata, record, rowIndex, colIndex, store )
{
        //return '<img src="' + gURLRoot + '/images/progress_bar_blank.png" alt="progress!" />';
        //return "<script>display('100','0');</script>"
        //value = colours array [R,G,B,W]
        return display(value[0]+value[1]+value[2]+value[3],value[0]+value[1],value[0]);
        //return displayProgress(value[0],value[1],value[2],value[3]);
}
function createNumItemsSelector(){
        var store = new Ext.data.SimpleStore({
                fields:['number'],
                data:[[25],[50],[100],[150]]
        });
        var combo = new Ext.form.ComboBox({
                allowBlank:false,
                displayField:'number',
                editable:false,
                maxLength:3,
                maxLengthText:'The maximum value for this field is 999',
                minLength:1,
                minLengthText:'The minimum value for this field is 1',
                mode:'local',
                name:'number',
                selectOnFocus:true,
                store:store,
                triggerAction:'all',
                typeAhead:true,
                value:50,
                width:50
        });
        combo.on({
                'collapse':function() {
                        var bb = gMainGrid.getBottomToolbar();
                        if( bb.pageSize != combo.value )
                        {
                                bb.pageSize = combo.value;
                                var store = gMainGrid.getStore()
                                store.load( { params : { start : 0, limit : bb.pageSize } } );
                        }
                }
        });
        return combo;
}

function cbMainGridSortChange( mainGrid, params )
{
        var store = mainGrid.getStore();
        store.setDefaultSort( params.field, params.direction );
        store.reload();
}

function rescheduleProject()
{
}

function killProject()
{
}

function toggleAll( select )
{
        var chkbox = document.getElementsByTagName('input');
        for (var i = 0; i < chkbox.length; i++)
        {
                if( chkbox[i].type == 'checkbox' )
                {
                        chkbox[i].checked = select;
                }
        }
}

function cbJumpFailed(a,b,c)
{
  gContextMenu.hide();
  jump(gContextMenu.project, 'Failed');
}


function cbJump(a,b,c)
{
  gContextMenu.hide();
  jump(gContextMenu.project, '');
}

function jump(project, status){
  var request = ''
  try{
    if (document.location.port != '')
    {
    var url = document.location.protocol + '//' + document.location.hostname + ':' +
              document.location.port + gURLRoot + '/' +
              gPageDescription.selectedSetup;
    }else{
    var url = document.location.protocol + '//' + document.location.hostname + gURLRoot + '/' +
              gPageDescription.selectedSetup;
    }
    url = url + '/' + gPageDescription.userData.group + '/jobs/JobMonitor/display';
    var post_req = '<form id="redirform" action="' + url + '" method="POST" >';
    post_req = post_req + '<input type="hidden" name="prod" value="' + project + '">';
    post_req = post_req + '<input type="hidden" name="status" value="' + status + '">';
    post_req = post_req + '<input type="hidden" name="start" value="0">';
    post_req = post_req + '<input type="hidden" name="sort" value="JobID DESC">';
    post_req = post_req + '<input type="hidden" name="limit" value="25">';
    post_req = post_req + '<input type="hidden" name="getStat" value="Status">';
    post_req = post_req + '</form>';
    document.body.innerHTML = document.body.innerHTML + post_req;
    var form = document.getElementById('redirform');
    form.submit();
  }catch(e){}
}

/* Revision of WebAppers Progress Bar, version 0.2
*  (c) 2007 Ray Cheung
*  WebAppers Progress Bar is freely distributable under the terms of an Creative Commons license.
*  For details, see the WebAppers web site: http://wwww.Webappers.com/
/*--------------------------------------------------------------------------*/

var initial = -119;
var imageWidth = 240;
var eachPercent = (imageWidth/2)/100;
var DIR_PATH_IMAGES = '/DIRAC/images/';

/************************************************************/
function setText (id, percent)
{
    $(id+'Text').innerHTML = percent+"%";
}

/************************************************************/
function display ( total, used, failed )
{	
    var percentage = 0;
    var color = 5; 
    if (total!='N/A' && used!='N/A') {
        total = parseInt(total);
        used  = parseInt(used);
        failed = parseInt(failed);
	    if (total != 0) percentage = parseInt(used * 100 / total);
	    else            percentage = 0;

            if (failed == 0)
            {
               color = "1";//green	
            }
            else if (failed == total)
            {
               color = "4";//red
            }
            else
            {
               color = "3";//orange
            };
	    //if      (percentage < 0)   color = "2"; //yellow
	    //else if (percentage < 80)  color = "1"; //green
	    //else if (percentage < 90)  color = "2"; //yellow
	    //else if (percentage < 101) color = "4"; //red
	    //else                       color = "2"; //yellow
    }
    
    var percentageWidth = 0;
    if (percentage < 0 || percentage > 100) percentageWidth = eachPercent * 100;
    else percentageWidth = eachPercent * percentage;
    var actualWidth = initial + percentageWidth;
    return('<img ' +
        'alt="'+percentage+'%" ' + 
        'src="'+DIR_PATH_IMAGES+'percentImage.png" ' + 
        'class="percentImage'+color+'" ' +
        'style="background-position: '+actualWidth+'px 0px;"/> ' +
        '<span>'+percentage+'%</span>');
}

function displayProgress ( red, green, blue, white )
{	
    var percentage = 0;
    var color = 5; 
    red = parseInt(red);
    green = parseInt(green);
    blue = parseInt(blue);
    white = parseInt(white);
    total = red+green+blue+white;
    percentage = parseInt(green * 100 / total);

    var percentageWidth = eachPercent * percentage;

    var greenWidth =  eachPercent  * (green*100/total);
    var blueWidth = eachPercent  * (blue*100/total);
    var redWidth = eachPercent  * (red*100/total);
    var whiteWidth = eachPercent  * (white*100/total);

    backImage = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage1px.png" ' + 
        'alt="'+percentage+'%" ' + 
        'class="percentImage1" ' +
        'style="background-position: '+greenWidth+'px 0px; width: '+greenWidth+'px;"/> ';
    blueImage = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage1px.png" ' + 
        'alt="'+percentage+'%" ' + 
        'class="percentImage2" ' +
        'style="background-position: '+(greenWidth+blueWidth)+'px 0px; width: '+blueWidth+'px;"/> ';
    redImage = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage1px.png" ' + 
        'alt="'+percentage+'%" ' + 
        'class="percentImage4" ' +
        'style="background-position: '+(blueWidth+greenWidth+redWidth)+'px 0px; width: '+redWidth+'px;"/> '+
        '<span>'+percentage+'%</span>';
   return backImage+blueImage+redImage;
}
function display_string( total, used, type)
{	
    var percentage = 0;
    var color = 5;
    if (total != 0) percentage = parseInt(used * 100 / total);

    if (type == "usedonline") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else if (type == "usednearline") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else if (type == "runningjobs") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 10)  color = "4"; //red
        else if (percentage < 20)  color = "2"; //yellow
        else if (percentage < 201) color = "1"; //green
        else                       color = "2"; //yellow
    } else if (type == "waitingjobs") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else {
        if      (percentage < 0)   color = "5"; //gray
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 95)  color = "3"; //orage
        else if (percentage < 101) color = "4"; //red
        else                       color = "5"; //gray 
    }

    var initial = -60;
    var imageWidth = 120;
    var eachPercent = (imageWidth/2)/100;
    var percentageWidth = 0;
    if (percentage < 0 || percentage > 100) percentageWidth = eachPercent * 100;
    else percentageWidth = eachPercent * percentage;
    var actualWidth = initial + percentageWidth;
    var content = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage_small.png" ' + 
        'alt="'+percentage+'%" ' + 
        'title="'+used+'" ' + 
        'class="percentImage'+color+'_small" ' +
        'style="background-position: '+actualWidth+'px 0px;"/> ' +
        '<span class="PercentageStatus'+color+'">'+percentage+'%</span>';
    return content;
}
