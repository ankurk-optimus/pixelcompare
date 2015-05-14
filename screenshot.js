var config = require('/home/local/OPTIMUSDOM/ubuntu90/Music/pixelcompare/Config.json');
var device = require('/home/local/OPTIMUSDOM/ubuntu90/Music/pixelcompare/Devices.json');
var page = require('webpage').create();

var snap = function (width, height, url){
    page.open(url, function(status) {
        console.log(url);
        console.log(width);
        console.log(height);
        console.log(status);
        page.render("hello.png");
        // page.render(config.projectName"//input//screenshots//"page1.pageName".png");
        phantom.exit();
    });
};

// config.subject.forEach(function(page1){
//     var url = page1.pageUrl;
//     page1.devices.forEach(function(dev){
//         var width = device[dev].width;
//         var height = device[dev].height;
//         snap(width, height, url);
//     });
// });

// snap(320, 2500, "http://www.headhonchos.com");
for(var i = 0, page1 = config.subject; i < page1.length; i++) {
    var url = page1[i].pageUrl;
    // console.log(page1[i].devices.length);
    for(var j=0, dev = page1[i].devices; j < dev.length; j++) {
        // console.log("dev[j]----++++++" + dev[j]);
        var dev1 = dev[j];
        var width = device[dev1].width;
        var height = device[dev1].height;
        snap(width, height, url);
    }
}

page.onError = function (msg, trace) {
    console.log(msg);
    trace.forEach(function(item) {
        console.log('  ', item.file, ':', item.line);
    });
};
