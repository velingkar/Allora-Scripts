// bouding array for cropping
var cropX = 500;
var cropY = 510;
var cropW = 300;
var cropH = 450;
var region = Array(cropX,cropY,cropX+cropW,cropY+cropH);

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");

if (inputFolder != null) {
    // get watermark 
    var watermarkPath = "C:\\Users\\Amit Velingkar\\TShirts\\Media\\Logos\\Watermark.png";
    var watermarkDoc = open(File(watermarkPath));
    watermarkDoc.activeLayer.copy();

    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");
    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            // open the file
            var curDoc = open(fileList[i]);

            // crop, resize and export
            curDoc.crop(region);
            curDoc.resizeImage(cropW*3,cropH*3);

            // paste water mark
            curDoc.paste();

            //export as PNG
            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            exportAsPNG(fileList[i].path + "/detail/",fileName + "_detail");

            // close doc without saving
            curDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    // close doc without saving
    watermarkDoc.close(SaveOptions.DONOTSAVECHANGES);

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
