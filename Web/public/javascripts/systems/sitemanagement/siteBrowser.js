
function initSiteBrowser(usersData){
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
    renderPage(usersData);
  });
}


function renderPage(usersData)
{

    Ext.define('User', {
        extend: 'Ext.data.Model',
        fields: [ 'name', 'email', 'dn' ]
    });

    var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: usersData,
    });

    var panel = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
    title: 'Application Users',
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
            text: 'Email Address',
            width: 150,
            dataIndex: 'email',
            hidden: false
        },
        {
            text: 'DN',
            flex: 1,
            dataIndex: 'dn'
        }
    ]
    });



  renderInMainViewport( [ panel ] );


}


function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}

