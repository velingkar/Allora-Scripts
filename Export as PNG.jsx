// save current preferences
var orgRulerUnits = app.preferences.rulerUnits;
var orgTypeUnits = app.preferences.typeUnits;
var orgDisplayDialogs = app.displayDialogs;

//set to use pixels and show no dialogs
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits  = TypeUnits.PIXELS;
app.displayDialogs  = DialogModes.NO;

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");

if (inputFolder != null) {
    // get all PNG files
    var fileList = inputFolder.getFiles("*.psd");
    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            // open the file
            var curDoc = open(fileList[i]);

            // add info
            curDoc.info.author = "Allorio Private Limited";
            curDoc.info.copyrightNotice = "Copyright (c) Allorio Private Limited";
            curDoc.info.copyrighted = CopyrightedType.COPYRIGHTEDWORK;

            //save as PNG
            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            saveAsPNG(fileList[i].path + "/PNG/",fileName);

            // close doc without saving
            curDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    // restore original settings
    app.preferences.rulerUnits = orgRulerUnits;
    app.preferences.typeUnits  = orgTypeUnits;
    app.displayDialogs  = orgDisplayDialogs;

    alert ("Export Completed !");
}

function saveAsPNG(filepath, filename) {
    var opts = new PNGSaveOptions();

    var exportFolder = Folder(filepath);
    if (!exportFolder.exists) exportFolder.create();

    var pngFile = new File(filepath + filename + ".png");
    app.activeDocument.saveAs(pngFile, opts);
}

// creates lossy files (72 dpi) - to be deprecated
/*
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
*/