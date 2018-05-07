$(document).ready(function() {
  // d3.selectAll("code").each(function() { hljs.highlightBlock(this); });
  // parseMd()
});

function parseMd() {
  var GITHUB = 'https://raw.githubusercontent.com/gto76/my-linux-setup/gh-pages/text-files/WTF-MAN'
  jQuery.get(GITHUB, function(text) {
    // var converter = new showdown.Converter()
    // html = converter.makeHtml(text)

    aDiv = $('#bla')
    nodes = $.parseHTML(html)
    aDiv.after(nodes);
    // insertLinks()
    d3.selectAll("code").each(function() { hljs.highlightBlock(this); });
  });
}


function convert(md) {
  
}

function insertLinks() {
  $('h2').each(function() {
    aId = $(this).attr('id')
    $(this).append('<a href="#'+aId+'" name="'+aId+'">#</a>')
  })
}
