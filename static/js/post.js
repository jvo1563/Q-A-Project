// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    answer: "",
    rows: [],
    answer_status: false,
    current_user: "",
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };
  app.set_answer_status = function (new_status) {
    app.vue.answer_status = new_status;
  };
  app.reset_form = function () {
    app.vue.answer = "";
  };
  app.add_answer = function () {
    axios
      .post(add_answer_url, {
        answer: app.vue.answer,
        post_id: post_id,
      })
      .then(function (response) {
        app.vue.rows.push({
          id: response.data.id,
          answer: app.vue.answer,
          user_email: response.data.user_email,
          time_answered: response.data.time_answered,
          name: response.data.name,
        });
        app.enumerate(app.vue.rows);
        app.reset_form();
        app.set_answer_status(false);
      });
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    set_answer_status: app.set_answer_status,
    reset_form: app.reset_form,
    add_answer: app.add_answer,
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
    axios.get(load_answers_url).then(function (response) {
      let rows = response.data.rows;
      app.enumerate(rows);
      app.vue.current_user = response.data.current_user;
      app.vue.rows = rows;
    });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
