// bouding array for cropping
var boundsX = 1 / 100; // move 1/100'th of image size
var boundsY = 1 / 200; // move 1/200'th of image size

// save current preferences
var orgRulerUnits = app.preferences.rulerUnits;
var orgTypeUnits = app.preferences.typeUnits;
var orgDisplayDialogs = app.displayDialogs;

//set to use pixels and show no dialogs
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits = TypeUnits.PIXELS;
app.displayDialogs = DialogModes.NO;

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with designs");

if (inputFolder != null) {
    // get all PNG files
    var fileList = inputFolder.getFiles("*.png");
    for (var i = 0; i < fileList.length; i++) {
        // TODO - Debug Code
        // if (i > 0) break;

        if (fileList[i] instanceof File) {
            // open the file
            var curDoc = open(fileList[i]);
            createWhiteBackground(curDoc); // create new white background

            // select first layer & change properties
            lay = curDoc.layers[0];
            var randRotate = 1.5 - Math.random() * 3; // -1.5 to 1.5
            lay.rotate(randRotate);
            var randX = (curDoc.width * boundsX) - Math.random() * (curDoc.width * boundsX * 2); // -20 to 20
            var randY = (curDoc.height * boundsY) - Math.random() * (curDoc.height * boundsY * 2); // -20 to 20
            lay.translate(randX, randY);
            var randSize = 100 + (5 - Math.random() * 10); // 95 to 105
            lay.resize(randSize, randSize);
            //alert("rotate: "+randRotate+" ,size: "+randSize+" ,X: "+randX+" ,Y: "+randY);

            //export as PNG
            var fileName = fileList[i].name.match(/(.*)\.[^\.]+$/)[1];
            exportAsPNG(fileList[i].path + "/jitter/", fileName);

            // close doc without saving
            curDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    // restore original settings
    app.preferences.rulerUnits = orgRulerUnits;
    app.preferences.typeUnits = orgTypeUnits;
    app.displayDialogs = orgDisplayDialogs;

    alert("Export Completed !");
}

function createWhiteBackground(curDoc) {
    // set previous background layer as false
    curDoc.layers[0].isBackgroundLayer = false;

    // add a new layer at the end, white background
    // Create color object of color red
    var fillColor = new SolidColor();
    fillColor.rgb.red = 255;
    fillColor.rgb.green = 255;
    fillColor.rgb.blue = 255;

    // Add a new layer called Background
    var layer = curDoc.artLayers.add();
    layer.name = "WhiteBG";
    // Select the entire layer
    curDoc.selection.selectAll()
    // Fill the selection with color
    curDoc.selection.fill(fillColor);
    layer.isBackgroundLayer = true;
}

function exportAsPNG(filepath, filename) {
    var opts = new ExportOptionsSaveForWeb();
    opts.format = SaveDocumentType.PNG;
    opts.PNG8 = false;
    opts.quality = 100;

    var exportFolder = Folder(filepath);
    if (!exportFolder.exists) exportFolder.create();

    var pngFile = new File(filepath + filename + ".png");
    app.activeDocument.exportDocument(pngFile, ExportType.SAVEFORWEB, opts);
}
