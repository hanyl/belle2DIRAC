var gMainGrid = false;
var gVMMenu = false;

function initSiteBrowser(){
  Ext.onReady(function(){
    renderPage();
  });
}


function renderPage()
{
        var panels = [];
        var mainTreePanels = createDSTree();
        for( var i=0; i< mainTreePanels.length; i++ )
        {
                panels.push( mainTreePanels[i] );
        }
        renderInMainViewport( panels );

}


function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}

