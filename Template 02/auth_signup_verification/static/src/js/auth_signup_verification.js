odoo.define('auth_signup_verification.signup_varification', function (require) {
    "use strict";

    require('web.dom_ready');
    
    /* Signup form submit click to check validation,
     * Given an error message while not validate field value 
     * after successfull validate default process trigger */
	$('.oe_signup_form').find("button[type='submit']").on('click', function (ev) {
		var form_name = $('.oe_signup_form');
		checkInputValidation(form_name);
		if($('.oe_signup_form').find(".error_message").length != 0){
			ev.preventDefault();
			ev.stopPropagation();
			return;
		}
	})
	
	/* Common input validation function for signup  
	 * Password Validation Function 
     * Password between 8 to 15 characters,
     * Must contain at least 1-lowercase letter, 1-uppercase letter, 1-numeric digit, and 1-special character*/
	function checkInputValidation(form_name){
		var validation_error = false;
		$(".error_message").remove();
		form_name.find("input[required='required']").each(function(){
			var self = $(this);
			if(self.val() == ''){
				self.after( "<span class='error_message text-warning'>Please fill in the blank</span> ");
				validation_error = true;
				return false;
			}else if(self.attr("name") == "login"){
				if(!isValidEmail(self.val())){ 
					self.after( "<span class='error_message text-warning'>Enter valid email address</span> ");
					validation_error = true;
					return false;
				}
			}else if(self.attr("name") == "password"){
				var password = self.val();
				if(password.length < 8) {
					self.after( "<span class='error_message text-warning'>Password is too small (Minimum length is 8)</span> ");
					validation_error = true;
					return false;
		        }
				if(password.length > 15) {
					self.after( "<span class='error_message text-warning'>Password length is bigger (Maximum length is 15)</span> ");
					validation_error = true;
					return false;
		        }
		        var re = /[0-9]/;
		        if(!re.test(password)) {
		        	self.after( "<span class='error_message text-warning'>Must contain at least 1 numeric digit</span> ");
					validation_error = true;
					return false;
		        }
		        re = /[a-z]/;
		        if(!re.test(password)) {
		        	self.after( "<span class='error_message text-warning'>Must contain at least 1 lowercase letter</span> ");
					validation_error = true;
					return false;
		        }
		        re = /[A-Z]/;
		        if(!re.test(password)) {
		        	self.after( "<span class='error_message text-warning'>Must contain at least 1 uppercase letter</span> ");
					validation_error = true;
					return false;
		        }
		        re = /[!@#$%^&*(),.?":{}|<>]/g;
		        if(!re.test(password)) {
		        	self.after( "<span class='error_message text-warning'>Must contain at least 1 special charactor</span> ");
					validation_error = true;
					return false;
		        }
			}else if(self.attr("name") == "confirm_password"){
				var password = $("input[name=password]").val();
				if(password != self.val()){
					self.after( "<span class='error_message text-warning'>Password does not match</span> ");
					validation_error = true;
					return false;
				}
			}else{
				self.siblings(".error_message").remove();
				validation_error = false;
			}
		})
	}
	
    /* Email validation */
	function isValidEmail(emailid) {
		var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	    return pattern.test(emailid);
	}
	
	/* Click on password field eye icon to show password into Sign Up form */
	$(".toggle-password").click(function() {
		var self = $(this);
		self.toggleClass("fa-eye fa-eye-slash");
		var input = self.parent(".field-password").find("#password");
		if (input.attr("type") == "password") {
			input.attr("type", "text");
		} else {
			input.attr("type", "password");
		}
	});
	
	/* Avoid to change the reset password email if you are logged in user
	 * Given an error message to not change email address and stop submit form */
	$('.oe_reset_password_form').find("button[type='submit']").on('click', function (ev) {
		if($(".default_login_user_email").length){
			var default_login_user_email = $(".default_login_user_email").html();
			var input_email = $(".change_password_input").val();
			if(default_login_user_email != input_email){
				$(".email_notchange_error_msg").removeClass("d-none");
				ev.preventDefault();
				ev.stopPropagation();
	            return;
			}else{
				$(".email_notchange_error_msg").addClass("d-none");
			}
		}else{
			var form_name = $('.oe_reset_password_form');
			checkInputValidation(form_name);
			if(form_name.find(".error_message").length != 0){
				ev.preventDefault();
				ev.stopPropagation();
				return;
			}
		}
	})
});


