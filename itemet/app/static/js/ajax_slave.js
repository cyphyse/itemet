//-----------------------------------------------------------
// AJAX REST call to server to fetch data for select2 Slaves
//-----------------------------------------------------------
function loadSelectManyDataSlave(elem) {
  $(".ajax_multi_slave").each(function(index) {
    // define function to update data via endpoint
    function updateOptionsViaEndpoint(opt, master_val, item_id) {
      var endpoint_opt = elem.attr('endpoint_opt');
      var endpoint_sel = elem.attr('endpoint_sel');
      endpoint_opt = endpoint_opt.replace("{{ID}}", master_val);
      endpoint_sel = endpoint_sel.replace("{{ID}}", item_id);
      $.get(endpoint_opt, function(options) {
        $.get(endpoint_sel, function(selection) {
          // remove entries
          opt.html("");
          // add entries from data
          options.forEach(function addOption(item, index) {
            var sel = false;
            selection.forEach(function(obj, idx) {
              if (parseInt(item.id) == parseInt(obj.id)) {
                sel = true;
              }
            });
            var newOption = new Option(item.text, item.id, false, sel);
            opt.append(newOption);
          });
          // update
          opt.trigger('change');
        });
      });
    }
    // connect all
    var elem = $(this);
    // initialize
    var master_id = elem.attr('master_id');
    var master_val = $('#' + master_id).val();
    var path = window.location.pathname.split('/')
    var item_id = path[path.length-1];
    if (master_val) { // ensure the field and value
      updateOptionsViaEndpoint(elem, master_val, item_id);
    }
    // update of entries on each change
    $('#' + master_id).on("change", function(e) {
      if (e.val) {
        updateOptionsViaEndpoint(elem, e.val, item_id);
      }
    })
  });
}



//---------------------------------------
// Setup select2 many
//---------------------------------------
$(document).ready(function() {
  loadSelectManyDataSlave();
});
