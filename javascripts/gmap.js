/*
 * Ext JS Library 2.2
 * Copyright(c) 2006-2008, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://extjs.com/license
 */


Ext.onReady(function(){

    var mapwin;
    var button = Ext.get('show-btn');

    button.on('click', function(){
        // create the window on the first click and reuse on subsequent clicks
        if(!mapwin){

            mapwin = new Ext.Window({
                layout: 'fit',
                title: 'GMap Window',
                closeAction: 'hide',
                width:400,
                height:400,
                x: 40,
                y: 60,
                items: {
                    xtype: 'gmappanel',
                    region: 'center',
                    zoomLevel: 14,
                    gmapType: 'map',
                    mapConfOpts: ['enableScrollWheelZoom','enableDoubleClickZoom','enableDragging'],
                    mapControls: ['GSmallMapControl','GMapTypeControl','NonExistantControl'],
                    setCenter: {
                        lat: 21.030994081751,
                        lng: 105.85249900818,
                        marker: {title: 'ngi vietnam'},
                        listeners: {
                            click: function(e){
                                Ext.Msg.alert('We\'re here!', 'You are more than welcome to drop by.');
                            }
                        }
                    }
                }
            });
            
        }
        
        mapwin.show();
        
    });
    
 });