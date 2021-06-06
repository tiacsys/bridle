function LPNB () {
  "use strict";

  let state = {};

  // XXX: do not remove the trailing '/'
  const BRIDLE_PATH_PREFIX = "/lpn-bridle/html/";
  const STABLE_VERSION_RE = /^(\d+\.)+\d+$/;
  const DEV_VERSION_RE = /^(\d+\.)+\d+-[a-z0-9]+$/;

  /*
   * Allow running from localhost; local build can be served with:
   * python -m http.server
   */
  state.updateLocations = function(){
    const host = window.location.host;
    if (host.startsWith("localhost")) {
      this.url_prefix = "/";
    } else {
      this.url_prefix = BRIDLE_PATH_PREFIX;
    }

    this.url_root = window.location.protocol + "//" + host + this.url_prefix;
    this.version_data_url = this.url_root + "latest" + "/versions.json";
  };

  /*
   * Find the index of the first element that matches a X.Y.Z release, this
   * is considered the last "official" release.
   */
  state.findLastVersionIndex = function() {
    const versions = window.LPNB.versions.VERSIONS;
    window.LPNB.last_version_index = 1;
    for (var index in versions) {
      if (STABLE_VERSION_RE.test(versions[index])) {
        window.LPNB.last_version_index = index;
        break;
      }
    }
  }

  /*
   * Infer the currently running version of the documentation
   */
  state.findCurrentVersion = function() {
    const path = window.location.pathname;
    if (path.startsWith(this.url_prefix)) {
      const prefix_len = this.url_prefix.length;
      window.LPNB.current_version = path.slice(prefix_len).split("/")[0];
    } else {
      window.LPNB.current_version = "latest";
    }
  };

  /*
   * Infer the current page being browsed, stripped from any fixed and
   * versioned prefix; it'll be used to jump to the same page in another
   * docset version.
   */
  state.findCurrentPage = function() {
    const path = window.location.pathname;
    const version_prefix = window.LPNB.current_version + "/";
    if (path.startsWith(this.url_prefix)) {
      const prefix_len = this.url_prefix.length;
      let new_page = path.slice(prefix_len);
      if (new_page.startsWith(version_prefix)) {
        new_page = new_page.slice(version_prefix.length);
      }
      window.LPNB.current_page = new_page;
    } else {
      window.LPNB.current_page = "lpnb/index.html";
    }
  };

  /*
   * Updates the dropbox of nRF Connect SDK versions displayed below the
   * current development version, and links to the same page currently being
   * browsed in those earlier releases.
   */
  state.updateVersionDropDown = function() {
    const lpnb = window.LPNB;
    const versions = lpnb.versions.VERSIONS;

    // Avoid applying DOM changes on errors
    const path = window.location.pathname;
    if (!path.startsWith(this.url_prefix)) {
      return;
    }

    // Only display dropdown for nRF Connect documentation set
    const prefix_len = this.url_prefix.length;
    if (path.slice(prefix_len).split("/")[1] !== "lpnb") {
      return;
    }

    let links = '';
    $.each(versions, function(_, v) {
      if (v !== lpnb.current_version) {
        links += "<li><a href=" + lpnb.url_root + v + "/" + lpnb.current_page +
          ">" + v + "</a></li>";
      }
    });

    $("div.version").append("<span class='fa fa-caret-down dropit'></span>" +
      "<ul class='dropdown'>" + links + "</ul>");

    // hide version dropdown by default & toggle
    $(".dropdown").hide();
    $(".dropit").click(function(){
      $(this).next(".dropdown").toggle();
    });
  };

  /*
   * Display a message at the top of the page to inform the user that the
   * version currently being browsed is not the latest.
   */
  state.showVersion = function() {
    const lpnb = window.LPNB;
    const VERSIONS = lpnb.versions.VERSIONS;
    const last_version_index = lpnb.last_version_index;
    const path_suffix = "/" +  lpnb.current_page;
    const last_release_url = lpnb.url_root + VERSIONS[last_version_index] + path_suffix;
    const latest_release_url = lpnb.url_root + "latest" + path_suffix;

    const SWITCH_MSG = "You might want to switch to the documentation for " +
      "the <a href='" + last_release_url + "'>" + VERSIONS[last_version_index] +
      "</a> release or the <a href='" + latest_release_url + "'>current " +
      "state of development</a>."

    const OLD_RELEASE_MSG =
      "You are looking at an older version of the documentation. " + SWITCH_MSG;

    const DEV_RELEASE_MSG =
      "You are looking at the documentation for a development tag. " + SWITCH_MSG;

    const LAST_RELEASE_MSG =
      "You are looking at the documentation for the latest official release.";

    if ($("#version_status").length === 0) {
      $("div[role='navigation'] > ul.wy-breadcrumbs").
        after("<div id='version_status'></div>");
    }

    if (lpnb.current_version === VERSIONS[0]) {
      $("div#version_status").hide();
    } else if (lpnb.current_version === VERSIONS[last_version_index]) {
      $("div#version_status").html(LAST_RELEASE_MSG);
    } else if (DEV_VERSION_RE.test(lpnb.current_version)) {
      $("div#version_status").html(DEV_RELEASE_MSG);
    } else {
      $("div#version_status").html(OLD_RELEASE_MSG);
    }
  };

  /*
   * Update the versions displayed in the documentation chooser
   */
  state.updateDocsetVersions = function() {
    const lpnb = window.LPNB;
    const current_version = lpnb.current_version;
    const by_version = lpnb.versions.COMPONENTS_BY_VERSION[current_version];

    let found = {};
    $.each(by_version, function(docset) {
      found[docset] = false;
    });

    // Update all versions but the one that is selected
    $('div.rst-other-versions').children('div').each(function (_, el) {
      $.each(by_version, function(docset, version) {
        if ($(el).hasClass(docset)){
          let a = $(el).children('a');
          a.text(a.text() + ' ' + version);
          found[docset] = true;
        }
      });
    });

    // Update the currently selected version
    $('span.rst-current-version > span.fa-book').each(function (_, el) {
      $.each(found, function(name, value) {
        if (!value) {
          $(el).text($(el).text() + ' ' + by_version[name]);
          return;
        }
      });
    });
  };

  state.updatePage = function() {
    let lpnb = window.LPNB;
    lpnb.findLastVersionIndex();
    lpnb.findCurrentVersion();
    lpnb.findCurrentPage();
    lpnb.updateVersionDropDown();
    lpnb.showVersion();
    lpnb.updateDocsetVersions();
  };

  const BRIDLE_SESSION_KEY = "lpnb";

  /*
   * Load a versions.json from the session cache if available
   */
  state.loadVersions = function() {
    let versions_data = window.sessionStorage.getItem(BRIDLE_SESSION_KEY);
    if (versions_data) {
      window.LPNB.versions = JSON.parse(versions_data);
      return true;
    }
    return false;
  }

  /*
   * Update the session cache with a new versions.json
   */
  state.saveVersions = function(versions_data) {
    let lpnb = window.LPNB;
    const session_value = JSON.stringify(versions_data);
    window.sessionStorage.setItem(BRIDLE_SESSION_KEY, session_value);
    window.LPNB.versions = versions_data;
  }

  /*
   * When the "Hide Search Matches" (from Sphinx's doctools) link is clicked,
   * rewrite the URL to remove the search term.
   */
  state.hideSearchMatches = function() {
    $('.highlight-link > a').on('click', function(){
      // Remove any ?highlight=* search querystring element
      window.location.assign(
        window.location.href.replace(/[?]highlight=[^#]*/, '')
      );
    });
  }

  return state;
};

if (typeof window !== 'undefined') {
  window.LPNB = LPNB();
}

$(document).ready(function(){
  window.LPNB.updateLocations();
  window.LPNB.hideSearchMatches();

  if (window.LPNB.loadVersions()) {
    window.LPNB.updatePage();
  } else {
    /* Get versions file from remote server. */
    $.getJSON(window.LPNB.version_data_url, function(json_data) {
      window.LPNB.saveVersions(json_data);
      window.LPNB.updatePage();
    });
  }
});
