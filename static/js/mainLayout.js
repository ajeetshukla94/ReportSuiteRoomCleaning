class MyHeader extends HTMLElement {
  connectedCallback() {
    var menu =
      '<div class="sidebar">\
			<ul>\
			  <li><img src="static/images/logo-wbg.png" id="header-img"></li>\
			  <li id="admin_grp">\
				<a href="#profile">\
				  <i class="fa fa-caret-down right"></i> ADMIN PANEL</a>\
				<ul>\
				  <li><a href="/add_user_page">ADD USER</a></li>\
				  <li><a href="/update_user_details_page">UPDATE USER DETAILS</a></li>\
				</ul>\
			  </li>\
			  <li id="room_cln_grp">\
				<a href="#Profile">\
				  <i class="fa fa-caret-down right"></i> ROOM CLEANING</a>\
				<ul>\
				  <li><a href="/cleaning_room">CLEANING ROOM</a></li>\
				  <li><a href="/UpdateProductList">UPDATE PRODUCT LIST</a></li>\
				  <li><a href="/download_report">DOWNLOAD REPORT</a></li>\
				  <li><a href="/render_elogbook">PRODUCT LOG</a></li>\
				</ul>\
			  </li>\
			  <li id="profile_grp">\
				<a href="#Profile">\
				  <i class="fa fa-caret-down right"></i> Profile</a>\
				<ul>\
				  <li><a href="/update_self_profile_page">PROFILE</a></li>\
				  <li><a href="/logout">LOGOUT</a></li>\
				</ul>\
			  </li>\
			</ul>\
		  </div>';

    this.innerHTML = menu;
  }
}
customElements.define("my-header", MyHeader);

class MyFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML =
      '<div id="footer"><h6 id="footer-text">Developed By &#169; Document Manager</h6></div>';
  }
}
customElements.define("my-footer", MyFooter);
