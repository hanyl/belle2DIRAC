var gMainGrid = false;
var gVMMenu = false;

function initDatasetTransfer(){
  Ext.onReady(function(){
    renderPage();
  });
}

function renderPage()
{
  gMainGrid = makeMainPanel();
  renderInMainViewport([gMainGrid]);
}

function makeMainPanel()
{
    //var datasetList = new Ext.data.SimpleStore({ fields: ['dataset'], data: [['e1hehe'], ['cakedata']]});
    //var siteList = new Ext.data.SimpleStore({ fields: ['site'], data: [['AU-PPS'], ['CAKE-LCG2']]});
    var datasetList = new Ext.data.JsonStore({
          autoLoad:true,
          fields:['dataset'],
          idProperty:'dataset',
          root:'datasets',
          url:'getDatasetList'
        }); 
 

    var siteList = new Ext.data.JsonStore({
          autoLoad:true,
          fields:['sitename'],
          idProperty:'sitename',
          root:'Value',
          url:'getSiteList'
        }); 
 

    var dataset = new Ext.form.ComboBox( {
        width:255,
        allowBlank : false,
        editable : true,
        typeAhead : true,
        triggerAction:'all',
        displayField: 'dataset',
        fieldLabel : 'Dataset',
        mode: 'local',
        store : datasetList,
        disabled : false } );



    //var fromSite = new Ext.form.ComboBox( {
    //    allowBlank : false,
    //    editable : false,
    //    triggerAction:'all',
    //    fieldLabel : 'From',
    //    mode: 'local',
    //    displayField:'sitename',
    //    store : siteList,
    //    disabled : false } );

    var toSite = new Ext.form.ComboBox( {
        width:255,
        allowBlank : false,
        editable : false,
        triggerAction:'all',
        fieldLabel : 'To',
        mode: 'local',
        displayField:'sitename',
        store : siteList,
        disabled : false } );

    var comment = new Ext.form.TextField( {
        width:255,
        allowBlank : false,
        editable : false,
        fieldLabel : 'Comment',
        disabled : false } );



        var frmPanel = new Ext.form.FieldSet ({
            title : 'Dataset Transfer',
            name : 'datasettransfer',
            collapsible : false,
            autoHeight : true,
            collapsed : false,
            hideBorders : false,
            //items : [dataset, fromSite, toSite],
            items : [dataset, toSite, comment],
          });

         var leftPanel = new Ext.FormPanel ({
                region : 'center',
                width : '100%',
                url : 'datasetTransfer',
                method : 'POST',
                items : [ frmPanel,
                        { layout : 'form',
                          border : false,
                          buttons : [ { text: 'Submit',
                                    handler : __submitTransferReq,
                                    },
                                    { text: 'Reset',
                                    handler: __resetFrmPanel,
                                    }
                                    ]
                        }
                        ]
        });

return leftPanel;

}

function __resetFrmPanel()
{
  alert('ResetFrmPanel not implemented!');
}

function __submitTransferReq()
{
  alert('submitTransferReq not implemented!');
}

function ajaxFailure( ajaxResponse, reqArguments )
{
        alert( "Error in AJAX request : " + ajaxResponse.responseText );
}
