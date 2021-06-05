// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    //bio: "",
    //bio_status: false,
    thumbnail: profile_picture,
    user_id: id,
  };

  /*app.set_bio_status = function (new_status) {
    app.vue.bio_status = new_status;
  };
  app.reset_form = function () {
    app.vue.answer = "";
  };
  app.add_bio = function () {
    axios
      .post(add_bio_url, {
        bio: app.vue.bio,
        auth_id: auth_id,
      })
      .then(function (response) {
        app.vue.rows.push({
          id: response.data.id,
          bio: app.vue.bio,
          auth_id: app.vue.auth_id,
          _state: { answer: "clean" },
        });
        app.enumerate(app.vue.rows);
        app.reset_form();
        app.set_answer_status(false);
      });
  };*/

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };
  app.upload_file = function (event) {
    let input = event.target;
    let file = input.files[0];
    if (file) {
      let reader = new FileReader();
      reader.addEventListener("load", function () {
        // Sends the image to the server.
        axios
          .post(upload_thumbnail_url, {
            user_id: app.vue.user_id,
            thumbnail: reader.result,
          })
          .then(function () {
            // Sets the local preview.
            app.vue.thumbnail = reader.result;
          });
      });
      reader.readAsDataURL(file);
    }
  };

  // This contains all the methods.
  app.methods = {
    upload_file: app.upload_file,
    // add_bio: app.add_bio,
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    // Put here any initialization code.
    // Typically this is a server GET call to load the data.
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
