/*
setInterval(                               //Periodically
  function()
  {
     $.getJSON(                            //Get some values from the server
        $SCRIPT_ROOT + '/map',      // At this URL
        {},                                // With no extra parameters
        function(data)                     // And when you get a response
        {
          $("#devices").text(data.result);  // Write the results into the
                                           // #result element
        });
  },
  1);                                    // And do it every 500ms
*/

function update_values() {
$SCRIPT_ROOT = {{ request.sctipt_root|tojson|safe }}

}