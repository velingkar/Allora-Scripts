// bouding array for cropping
var cropW = 700;
var cropH = 700;
var cropX = 1024 - (cropW / 2);
var cropY = 450;
var region = Array(cropX,cropY,cropX+cropW,cropY+cropH);
var scale = 3; // scale image by x

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
    // get watermark 
    // var watermarkPath = "C:\\Users\\Amit Velingkar\\TShirts\\Media\\Logos\\Watermark.png";
    // var watermarkDoc = open(File(watermarkPath));
    // watermarkDoc.activeLayer.copy();

    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");
    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            // open the file
            var curDoc = open(fileList[i]);

            // crop, resize and export
            curDoc.crop(region);
            curDoc.resizeImage(cropW*scale,cropH*scale);

            // paste water mark
            // curDoc.paste();

            //export as PNG
            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            exportAsPNG(fileList[i].path + "/detail/",fileName + "_detail");

            // close doc without saving
            curDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    // close doc without saving
    // watermarkDoc.close(SaveOptions.DONOTSAVECHANGES);

    // restore original settings
    app.preferences.rulerUnits = orgRulerUnits;
    app.preferences.typeUnits  = orgTypeUnits;
    app.displayDialogs  = orgDisplayDialogs;

    alert ("Export Completed !");
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
