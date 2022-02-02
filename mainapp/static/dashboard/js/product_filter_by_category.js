$(document).ready(function(){
      $("#id_category").change(function(){
            // Get the selected category name from <select>
            var cat = $(this).find('option').filter(':selected').text();
            // Fetch all the options for products
            var options = $("#id_product option")
            // Iterate the options
            $.map(options, function(option){
                  // Match the category name with the product category
                  var temp = option.outerText.match(cat)
                  // Show the matched items only
                  $(option).attr('style', (cat == temp) ? 'display:block' : 'display:none')
            })
      });
      $("#searchBox_update_price").keyup(function(){
            // Get the search box value
            var srch = this.value;
            // Fetch all the options for products
            var options = $("#id_products option");
            // Iterate the options
            $.map(options, function(option){
                  // Get the option outerText and match
                  var text = option.outerText;
                  var temp = text.toLowerCase().match(srch);
                  // Display the matched items
                  $(option).attr('style', (srch == temp) ? 'display:block' : 'display:none')
            })
      });
      $("#searchBox_add_product").keyup(function(){
            // Get the search box value
            var srch = this.value; 
            // Fetch all the options for products
            var options = $("#id_product option");
            // Iterate the options
            $.map(options, function(option){
                  // Get the option outerText and match
                  var text = option.outerText;
                  var temp = text.toLowerCase().match(srch);
                  // Display the matched items
                  $(option).attr('style', (srch == temp) ? 'display:block' : 'display:none')
            })
      });

      var d = new Date();
      var strDate = d.getFullYear() + "-" + ( (d.getMonth() + 1) > 9 ? (d.getMonth() + 1) : "0"+(d.getMonth() + 1) ) + "-" + d.getDate();
      $("input[type=date]").attr("max", strDate);

      $("#start_date_revenue_report").change(function(e){
            $("#end_date_revenue_report").attr("min", e.target.value);
      });

      $("#id_body").attr("required", true);
      $("#id_notification_type").attr("required", true);
      $("#div_id_offers").css("display", "none");
      $("#div_id_order").css("display", "none");

      $("#id_notification_type").change(function(){
            if(this.value == "offers"){
                  $("#div_id_offers").css("display", "block");
                  $("#id_offers").attr("required", true);
                  $("#div_id_order").css("display", "none");
                  $("#id_order").attr("required", false);
            }
            else{
                  $("#div_id_order").css("display", "block");
                  $("#id_order").attr("required", true);
                  $("#div_id_offers").css("display", "none");
                  $("#id_offers").attr("required", false);
            }
      });

      $("#id_unit_type").change(function(){
            var value = this.value;
            if(value == "3" || value == "4"){
                  $("#div_id_weight_in_grams").css("display", "block");
            }
            else{
                  $("#div_id_weight_in_grams").css("display", "none");
            }
      });

      $("#id_district").change(function(){
            console.log(this.value);
            $("#id_district").attr("disabled", true);
            $("#id_region").attr("disabled", true);
            $("#id_region").empty();
            $.ajax({
                  "url": "/store/get-service-pincodes/",
                  "type": "GET",
                  "data": {"district": this.value, "user": $("#user_id")[0].value},
                  "success": function(data){
                        data.forEach(element => {
                              $("#id_region").append(new Option(element, element))
                        });
                        $("#id_district").attr("disabled", false);
                        $("#id_region").attr("disabled", false);
                  }
            });
      });

      $("#id_region").change(function(){
            console.log(this.value);
            $.ajax({
                  "url": "/store/get-service-pincodes/",
                  "type": "GET",
                  "data": {"district": $("#id_district")[0].value, "city": this.value, "user": $("#user_id")[0].value},
                  "success": function(data){
                        var form = $("#add-pincode-form");
                        form.empty();
                        
                        var ul = $("<ul></ul>");
                        ul.attr("id", "ul-pincode");
                        form.append(ul);
                        
                        data.forEach(element => {   
                              var li = $("<li></li>");
                              ul.append(li);
                              
                              var div = $("<div> </div>").addClass("form-check");
                              li.append(div);
                              
                              var checkbox = $("<input type='checkbox'>");
                              checkbox.attr("name", "pincode");
                              checkbox.addClass("form-check-input");
                              checkbox.attr("id", element.placeName);
                              checkbox.val(element.placeName);
                              div.append(checkbox);
                              
                              var label = $("<label for='check1'></label>").addClass("form-check-label");
                              label.text(element.placeName+" - "+element.postalCode);
                              div.append(label);
                        });
                  }
            });
      });

      $("#id_discount_type").val("percent");
      $("#id_discount_type").change(function(){
            if(this.value == "percent"){
                  $("#div_id_flat").css("display", "none");
                  $("#div_id_percent").css("display", "block");
            }
            else{
                  $("#div_id_flat").css("display", "block");
                  $("#div_id_percent").css("display", "none");
            }
      });

      if($("#id_method").val() == "price"){
            $("#div_id_threshold").css("display", "none");
      }
      else{
            $("#div_id_threshold").css("display", "block");
      }

      $("#id_method").change(function(){
            if(this.value == "price"){
                  $("#div_id_threshold").css("display", "none");
            }
            else{
                  $("#div_id_threshold").css("display", "block");
            }
      });

      if($("#id_method").val() == "distance"){
            $("#div_id_free_delivery_above").css("display", "none");
            $("#div_id_free_delivery_below").css("display", "block");
      }
      else{
            $("#div_id_free_delivery_above").css("display", "block");
            $("#div_id_free_delivery_below").css("display", "none");
      }

      $("#id_method").change(function(){
            if(this.value == "distance"){
                  $("#div_id_free_delivery_above").css("display", "none");
                  $("#div_id_free_delivery_below").css("display", "block");
            }
            else{
                  $("#div_id_free_delivery_above").css("display", "block");
                  $("#div_id_free_delivery_below").css("display", "none");
            }
      });

      
      $("#chat-circle").click(function(){
            document.getElementById("myForm").style.display = "block";
            document.getElementById("chat-circle").style.display = "none";  
      });

      $("#close-bot").click(function() {
            document.getElementById("myForm").style.display = "none";
            document.getElementById("chat-circle").style.display = "block";
      });
});

