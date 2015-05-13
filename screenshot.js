var obj = require('/home/local/OPTIMUSDOM/ubuntu90/Music/pixelcompare/Config.json');

// var config = JSON.parse(obj);

var page = require('webpage').create();
var l;
// page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';


page.open("http://www.headhonchos.com", function(status) {
//     page.includeJs('https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js', function() {
//         // https://cdnjs.cloudflare.com/ajax/libs/log4javascript/1.4.9/log4javascript.js
//         page.evaluate(function() {
//         l = document.getElementById('#authorize');
//         console.log(l);
//         // var $btn = ($('#authorize'));
//         l.submit();
//     });
// });
//     console.log(l);
    console.log(obj.projectName);
    obj.subject.forEach(function(page){
            console.log(page.pageName);
        });
    console.log(obj.page-url);
    console.log('Status: ' + status);
    console.log(page.title);
    page.render(page.title+('.png'));
    phantom.exit();
});

page.onError = function (msg, trace) {
    console.log(msg);
    trace.forEach(function(item) {
        console.log('  ', item.file, ':', item.line);
    });
};
