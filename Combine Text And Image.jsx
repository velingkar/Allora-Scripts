// Simple Replace Image in a Text + Image PSD, Then Export

// get the designlayer
var designLayer = app.activeDocument.layers.getByName("MyDesign"); // design layer

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");
if (inputFolder != null && designLayer != null) {
    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");

    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            replaceImage(fileList[i], designLayer);

            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            // alert (fileList[i].path + "/media/" + ", path " + fileName);
            exportAsPNG(fileList[i].path + "/designs/",fileName);
        }
    }

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
