
function initGrid(sitesData){
//  Ext.require('Ext.panel.Panel');
//  Ext.require('Ext.toolbar.TextItem');
//  Ext.require('Ext.container.Viewport');
//  Ext.require('Ext.button.Split');
//  Ext.require('Ext.layout.container.Border');
  Ext.require([
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.state.*'
  ]);
  Ext.onReady(function(){
    renderPage(sitesData);
  });
}


function renderPage(usersData)
{

    Ext.define('User', {
        extend: 'Ext.data.Model',
        fields: [ 'name', 'status', 'swver', 'comment' ]
    });

    var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: usersData,
    });

    var panel = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
    title: 'Sites Management',
    region : 'center',
    columns: [
        {
            text: 'Name',
            width: 100,
            sortable: false,
            hideable: false,
            dataIndex: 'name'
        },
        {
            text: 'Status',
            width: 100,
            dataIndex: 'status',
            hidden: false
        },
        {
            text: 'basf2 version',
            width: 100,
            dataIndex: 'swver'
        },
        {
            text: 'Comment',
            flex: 1,
            dataIndex: 'comment'
        }
    ]
    });



  renderInMainViewport( [ panel ] );


}


function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}

