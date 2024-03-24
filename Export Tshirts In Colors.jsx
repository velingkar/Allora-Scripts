// get the designlayer
// V2.0 - Multiple Designs Style as per colors (Light, Dark etc.)
// add to PS path (example - C:\Program Files\Adobe\Adobe Photoshop 2024\Presets\Scripts)
var templatePath = "C:\\Users\\Amit Velingkar\\TShirts\\PSD Templates\\T-Shirt-Hanging-Mockup-v2.2.psd";

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with styles");
if (inputFolder != null) {
    // open the template and layers
    var templateDoc = open(File(templatePath));
    var lays = templateDoc.layers;
    var designLayer = lays[0].layers.getByName("MyDesign"); // design layers
    var bgLays = lays[1].layers; // background layers
    var colors = bgLays[2].layers; // color layers
    if(designLayer != null && colors != null) {
        // get all PNG files
        var fileList = inputFolder.getFiles("*.png");

        // iterate through all the color layers
        var lastStyle = ""; // optimisation to avoid needless image replace
        for (var i=0; i< fileList.length; i++) {
            if (fileList[i] instanceof File) {
                var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
                for (var j=0; j< colors.length; j++) {
                    if (j>0) colors[j-1].visible = false; // make previous layer invisible
                    colors[j].visible = true; // make new color layer visisble

                    var layerInfo = colors[j].name.split("_");
                    var colorName = layerInfo[0];
                    var styleName = layerInfo[1];

                    if (lastStyle != styleName) {
                        // replace the image
                        // TIP: In Template File, keep same style colors (light / dark) consecutively for less switches
                        replaceImage(fileList[i].path+"/designs/"+styleName+"/"+fileName+".png", designLayer);
                    }

                    // export image
                    exportAsPNG(fileList[i].path + "/media/",fileName + "_" + colorName);
                }
            }
        }
    }
    // close doc without saving
    templateDoc.close(SaveOptions.DONOTSAVECHANGES);
    alert ("Export Completed !");
}

function replaceImage(newFile, smartLayer) {
    app.activeDocument.activeLayer = smartLayer;
    var idplacedLayerReplaceContents = stringIDToTypeID("placedLayerReplaceContents");
    var desc3 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    desc3.putPath(idnull, new File(newFile));
    var idPgNm = charIDToTypeID("PgNm");
    desc3.putInteger(idPgNm, 1);
    executeAction(idplacedLayerReplaceContents, desc3, DialogModes.NO);
    return app.activeDocument.activeLayer
}

function exportAsPNG(filepath, filename) {
    var opts     = new ExportOptionsSaveForWeb();
    opts.format  = SaveDocumentType.PNG;
    opts.PNG8    = false;
    opts.quality = 100;

    var exportFolder = Folder(filepath);
    if (!exportFolder.exists) exportFolder.create();

    var pngFile = new File(filepath + filename + ".png");
    app.activeDocument.exportDocument(pngFile, ExportType.SAVEFORWEB, opts);
}
