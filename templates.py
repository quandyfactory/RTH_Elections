default = """
<div id="wrap">
    <div id="banner">
        <div class="right">
            <div class="current-date">
                [[date]] | [[time]]
            </div>
        </div>
        <div class="logo">
            <a href="/" title="Home">
                <img alt="Logo-banner" src="/static/images/logo-banner-elect.png">
            </a>
        </div>
        <div class="spacer">
        </div>
    </div>
    <div id="menu">
        <div id="search">
            <form id="searchform" name="searchform" method="get" action="http://www.google.com/search">
            <div>
                <input type="hidden" name="ie" value="utf-8">
                <input type="hidden" name="oe" value="utf-8">
                <input class="field" type="text" name="q" maxlength="255" title="Enter search terms here">
                <input class="button" type="submit" name="btng" value="" title="Search">
                <input type="hidden" name="domains" value="elections.raisethehammer.org">
                <input type="hidden" name="sitesearch" value="elections.raisethehammer.org">
            </div>
        </form>
    </div>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/elections">Elections</a></li>
        <li><a href="/wards">Ward Maps</a></li>
        <li><a href="/results">Results</a></li>
        <li><a href="/apidoc">API Documentation</a></li>
        <li><a href="/api" target="_blank">API</a></li>
    </ul>
</div>
<div id="content">
    <div id="column-wide">
        <div id="article">
            <div class="header">
                <h3>[[section]]</h3>
                <h1>[[title]]</h1>
                <div class="description">[[description]]</div>
            </div>
            <div class="content">[[content]]</div>
        </div>
        <div class="header" id="footer">
        <h3 class="black"><a href="#">Back to Top</a></h3>
        <div class="spacer"></div>
        <div class="logo"><img alt="Logo-footer" src="/static/images/logo-footer.png"></div>
        <div>
            <a title="Visit our main website" href="http://raisethehammer.org">Raise The Hammer</a><br>
            Copyright &copy; 2004-2010 | <a href="mailto:editor@raisethehammer.org">Contact Us</a>
        </div>
    </div>
</div>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-18580045-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type =
'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' :
'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(ga, s);
  })();

</script>
"""
