var gMainGrid = false;
var gVMMenu = false;

function initSiteBrowser(){
  Ext.onReady(function(){
    renderPage();
  });
}


function renderPage()
{

  var myReader = new Ext.data.ArrayReader({}, [
               {name: 'site'},
  ]);

  var store = new Ext.data.Store({
    reader: myReader
  });

  var columns = [
    {header:'',name:'checkBox',id:'checkBox',width:26,sortable:false,dataIndex:'lastChange',hideable:false,fixed:true,menuDisabled:true},
    {header:'Site',sortable:true,dataIndex:'lastChange',align:'left',hideable:false},
   ];

  gMainGrid = new Ext.grid.GridPanel( {store: store, columns: columns, region: 'center' } );
  renderInMainViewport([gMainGrid]);

}


function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}

