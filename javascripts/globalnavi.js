function active_menu(doc) {
    var re_result = location.href.match( /^https?:\/\/[^\/]+\/(ja\/|vi\/)?([^\/\?#]+).*$/ );

    var current_contents_name;
    if(re_result == null || !re_result.length || re_result.length < 2 || re_result[2] == 'ja' || re_result[2] == 'vi') {
        current_contents_name = 'home'
    } else {
        current_contents_name = re_result[2]
    }

    if(!current_contents_name) return;

    var target_tag = document.getElementById(current_contents_name);

    if(target_tag)
        target_tag.className = 'active'
}
