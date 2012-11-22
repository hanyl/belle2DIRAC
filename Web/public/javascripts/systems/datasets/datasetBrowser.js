var gMainGrid = false;
var gVMMenu = false;

function initDatasetBrowser(){
  Ext.onReady(function(){
    renderPage();
  });
}

function renderPage()
{
	var panels = [];
	//var leftBar = createLeftPanel( panels );
	var mainTreePanels = createDSTree();
	//var panels = [ leftBar ];
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
