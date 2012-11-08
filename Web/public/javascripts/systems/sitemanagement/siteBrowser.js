
function initSiteBrowser(){
//  Ext.require('Ext.panel.Panel');
//  Ext.require('Ext.toolbar.TextItem');
//  Ext.require('Ext.container.Viewport');
//  Ext.require('Ext.button.Split');
//  Ext.require('Ext.layout.container.Border');
  Ext.onReady(function(){
    renderPage();
  });
}


function renderPage()
{


  var mainPanel = Ext.create( 'Ext.panel.Panel', {
    title : 'Hello Ext4',
    region : 'center'
    } );
  console.log( "HLLO" );

  renderInMainViewport( [ mainPanel ] );


}


function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}

