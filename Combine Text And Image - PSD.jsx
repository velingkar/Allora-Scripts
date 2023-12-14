// Simple Replace Image in a Text + Image PSD, Then Export
// Version 2.0 - Multiple Designs as per colors (Light, Dark etc.)
// add to PS path (example - C:\Program Files\Adobe\Adobe Photoshop 2023\Presets\Scripts)
// get the designlayer
var designLayer = app.activeDocument.layers.getByName("MyDesign"); // design layer
var captionLayer = app.activeDocument.layers.getByName("Caption"); // caption text layer

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");
if (inputFolder != null && designLayer != null && captionLayer != null) {
    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");

    // get all captions
    var captions = captionLayer.layers; // get all captions in different colors

    // let us do some prep work
    var exportFolderPath = inputFolder.path + "/" + inputFolder.name +"/designs/"; 
    createExportFolder(exportFolderPath); // create designs folder
    // let us make all captions layers invisible & create folders with their names 
    for (var j=0; j< captions.length; j++) {
        captions[j].visible = false;
        createExportFolder(exportFolderPath + captions[j].name);
    }
    
    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            replaceImage(fileList[i], designLayer);

            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            // alert (fileList[i].path + "/media/" + ", path " + fileName);
            
            // step 1. let us make all captions invisible 
            for (var j=0; j< captions.length; j++) captions[j].visible = false;

            // step 2. let us make each caption visisble and export 
            for (var j=0; j< captions.length; j++) {
                if (j>0) captions[j-1].visible = false; // make previous layer invisible
                captions[j].visible = true;
                saveAsPSD(exportFolderPath + captions[j].name,fileName);
            }
        }
    }

    alert ("Export Completed !");
}

function createExportFolder(filepath) {
    var exportFolder = Folder(filepath);
    if (!exportFolder.exists) exportFolder.create();
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

function saveAsPSD(filepath, fileName) {
    var opts = new PhotoshopSaveOptions();
    opts.layers = true;
    opts.embedColorProfile = true;
    opts.spotColors = true;

    var psdFile = new File(filepath + "/" + fileName + ".psd");

    app.activeDocument.saveAs(psdFile,opts,true);

}

function exportAsPNG(filepath, filename) {
    var opts     = new ExportOptionsSaveForWeb();
    opts.format  = SaveDocumentType.PNG;
    opts.PNG8    = false;
    opts.quality = 100;

    var pngFile = new File(filepath + "/" + fileName + ".png");
    app.activeDocument.exportDocument(pngFile, ExportType.SAVEFORWEB, opts);
}
