// dpi value to save print
var dpi = 300; // save to 300 dpi
var scale = 1; // save N times the size
var resMethod = ResampleMethod.BICUBIC;

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");

if (inputFolder != null) {
    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");
    for (var i=0; i< fileList.length; i++) {
        if (fileList[i] instanceof File) {
            // open the file
            var curDoc = open(fileList[i]);


            // resize and export
            curDoc.resizeImage(curDoc.width*scale,curDoc.height*scale,300,resMethod);

            //export as PNG
            var fileName =  fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            exportAsPNG(fileList[i].path + "/HighRes/",fileName);

            // close doc without saving
            curDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
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
