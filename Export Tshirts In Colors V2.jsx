// get the designlayer
// V2.0 - Multiple Designs Style as per colors (Light, Dark etc.)
// add to PS path (example - C:\Program Files\Adobe\Adobe Photoshop 2024\Presets\Scripts)
var templatePath = "C:\\Users\\Amit Velingkar\\TShirts\\PSD Templates\\Tshirt_Mockup_v3.5.psd";

// Ask user for input folder
var inputFolder = Folder.selectDialog("Select folder with styles organized by color names");
if (inputFolder != null) {
    // open the template and layers
    var templateDoc = open(File(templatePath));
    var lays = templateDoc.layers;
    var designLayer = lays[0].layers.getByName("MyDesign"); // design layers
    var grpColorLayer = lays[0].layers.getByName("TShirt Color"); // color group layers
    var colors = grpColorLayer.layers; // color layers
    if (designLayer == null) alert("ERROR: myDesign layer NOT found in file!!!");
    if (colors == null) alert("ERROR: color layers NOT found in file!!!");
    if(designLayer != null && colors != null) {
        // iterate through color layers
        for (var i=0; i< colors.length; i++) {
            if (i>0) colors[i-1].visible = false; // make previous layer invisible
            colors[i].visible = true; // make new color layer visisble
            
            // open the "color" folder with design files
            var colorFolder = Folder(inputFolder.path + "/" + inputFolder.name + "/" + colors[i].name +"/");
            if (colorFolder == null) alert("ERROR: color folder "+ colorFolder.path +" NOT found in directory!!!");
            if (colorFolder != null) {
                var fileList = colorFolder.getFiles("*.png"); // get all PNG files
                for (var j=0; j< fileList.length; j++) {

                    if (fileList[j] instanceof File) {
                        var fileName =  fileList[j].name.match(/(.*)\.[^\.]+$/)[1]; // Extract file name
                        // TODO - add sanity check to see if _light or _dark is part of file name
                        var designName = splitLastOccurrence(fileName,"_")[0]; // discard _light,_dark
                        
                        // replace the image
                        replaceImage(fileList[j].path+"/"+fileList[j].name, designLayer);

                        // export image
                        exportAsPNG(colorFolder.path + "/media/"+ "/" + colors[i].name +"/",designName + "_" + colorFolder.name);
                    }
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

function splitLastOccurrence(str, substring) {
    const lastIndex = str.lastIndexOf(substring);
  
    const before = str.slice(0, lastIndex);
  
    const after = str.slice(lastIndex + 1);
  
    return [before, after];
  }
