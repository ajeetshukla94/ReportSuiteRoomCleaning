
class MyHeader extends HTMLElement{
	
	connectedCallback()	{						   
		var menu = '<nav class="animated bounceInDown bg-dark">\
						<ul>\
							<li><img src="static/images/logo.png" id="header-img"></li>\
							<li id="admin_grp" class="sub-menu"><a href="#profile">ADMIN PANEL<div class="fa fa-caret-down right"></div></a>\
								<ul>\
									<li><a href="/add_user_page">ADD USER</a></li>\
									<li><a href="/update_user_details_page">UPDATE USER DETAILS</a></li>\
								</ul>\
							</li>\
							<li id="room_cln_grp" class="sub-menu"><a href="#Profile">ROOM CLEANING<div class="fa fa-caret-down right"></div></a>\
							<ul>\
									<li><a href="/cleaning_room">CLEANING ROOM</a></li>\
									<li><a href="/UpdateProductList">UPDATE PRODUCT LIST</a></li>\
									<li><a href="/download_report">DOWNLOAD REPORT</a></li>\
									<li><a href="/render_elogbook">PRODUCT LOG</a></li>\
									</ul>\
							</li>\
							<li id="profile_grp" class="sub-menu"><a href="#Profile">Profile<div class="fa fa-caret-down right"></div></a>\
							<ul>\
									<li><a href="/update_self_profile_page">PROFILE</a></li>\
									<li><a href="/logout">LOGOUT</a></li>\
						    </ul>\
							</li>\
						</ul>\
					</nav>'
		
		this.innerHTML = menu
		
	}
}
customElements.define('my-header',MyHeader)


class MyFooter extends HTMLElement
{	
	connectedCallback()
	{
		this.innerHTML ='<div id="footer"><h6 id="footer-text">Developed By &#169; Document Manager</h6></div>'
	}
}
customElements.define('my-footer',MyFooter)

