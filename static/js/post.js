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
    post_final: 0,
    post_title: "",
    post_text: "",
    post_name: "",
    post_time_asked: "",
    post_category: "",
    post_id: "",
    post_email: "",
    post_rating: 0,
    post_edit_status: "clean",
    post_user_id: post_user_id,
    post_download_url: "",
    url: url,
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
          answer_user_email: response.data.user_email,
          time_answered: response.data.time_answered,
          name: response.data.name,
          final: 0,
          rating: 0,
          post_id: app.vue.post_id,
          _state: { answer: "clean" },
          user_id: response.data.user_id,
          download_url: response.data.download_url,
        });
        app.enumerate(app.vue.rows);
        app.reset_form();
        app.set_answer_status(false);
      });
  };

  app.set_rating = (rating) => {
    app.vue.post_rating = rating;
    axios
      .post(set_rating_url, { post_id: app.vue.post_id, rating: rating })
      .then(() => {
        axios
          .get(get_likers_url, { params: { post_id: app.vue.post_id } })
          .then((result) => {
            app.vue.post_final = result.data.likers;
          });
      });
  };
  app.setup_rating = (answers) => {
    // Initializes rating for post
    answers.map((answer) => {
      answer.rating = 0;
      answer.final = 0;
      answer._state = { answer: "clean" };
      axios
        .get(get_answer_thumbnail_url, {
          params: { email: answer.answer_user_email },
        })
        .then(function (response) {
          answer.user_id = response.data.user_id;
        });
    });
  };

  app.set_answer_rating = (row_idx, rating) => {
    let answer = app.vue.rows[row_idx];
    answer.rating = rating;
    axios
      .post(set_answer_rating_url, { answer_id: answer.id, rating: rating })
      .then(() => {
        axios
          .get(get_answer_likers_url, { params: { answer_id: answer.id } })
          .then((result) => {
            answer.final = result.data.final;
          });
      });
  };

  app.delete_post = function (post_id) {
    axios.get(delete_post_url, { params: { id: post_id } });
    location.href = "/qa/index";
  };
  app.delete_answer = function (row_idx) {
    let id = app.vue.rows[row_idx].id;
    axios
      .get(delete_answer_url, { params: { id: id } })
      .then(function (response) {
        for (let i = 0; i < app.vue.rows.length; i++) {
          if (app.vue.rows[i].id === id) {
            app.vue.rows.splice(i, 1);
            app.enumerate(app.vue.rows);
            break;
          }
        }
      });
  };
  app.start_answer_edit = function (row_idx) {
    app.vue.rows[row_idx]._state.answer = "edit";
  };
  app.stop_answer_edit = function (row_idx) {
    let row = app.vue.rows[row_idx];
    if (row._state.answer === "edit") {
      row._state.answer = "pending";
      axios
        .post(edit_answer_url, {
          id: row.id,
          field: "answer",
          value: row.answer, // row.first_name
        })
        .then(function (result) {
          row._state.answer = "clean";
        });
    }
    // If I was not editing, there is nothing that needs saving.
  };

  app.start_post_edit = function () {
    app.vue.post_edit_status = "edit";
  };
  app.stop_post_edit = function () {
    if (app.vue.post_edit_status === "edit") {
      app.vue.post_edit_status = "pending";
      axios
        .post(edit_post_url, {
          id: app.vue.post_id,
          field: "text",
          value: app.vue.post_text,
        })
        .then(function (result) {
          app.vue.post_edit_status = "clean";
        });
    }
    // If I was not editing, there is nothing that needs saving.
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    set_answer_status: app.set_answer_status,
    reset_form: app.reset_form,
    add_answer: app.add_answer,
    start_answer_edit: app.start_answer_edit,
    stop_answer_edit: app.stop_answer_edit,
    start_post_edit: app.start_post_edit,
    stop_post_edit: app.stop_post_edit,
    delete_post: app.delete_post,
    delete_answer: app.delete_answer,
    set_rating: app.set_rating,
    set_answer_rating: app.set_answer_rating,
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
    axios
      .post(load_answers_url, { post_id: post_id })
      .then(function (response) {
        let rows = response.data.rows;
        app.enumerate(rows);
        app.setup_rating(rows);
        app.vue.current_user = response.data.current_user;
        app.vue.rows = rows;
        app.vue.post_final = response.data.final;
        app.vue.post_title = response.data.title;
        app.vue.post_text = response.data.text;
        app.vue.post_time_asked = response.data.time_asked;
        app.vue.post_category = response.data.category;
        app.vue.post_name = response.data.name;
        app.vue.post_id = response.data.id;
        app.vue.post_rating = response.data.rating;
        app.vue.post_email = response.data.post_email;
      })
      .then(() => {
        for (let answer of app.vue.rows) {
          axios
            .get(get_answer_rating_url, { params: { answer_id: answer.id } })
            .then((result) => {
              answer.rating = result.data.rating;
              answer.final = result.data.final;
            });
          axios
            .get(post_pictures_url, {
              params: { email: answer.answer_user_email },
            })
            .then(function (r) {
              answer.download_url = r.data.download_url;
            });
        }
        axios
          .get(post_pictures_url, {
            params: { email: app.vue.post_email },
          })
          .then(function (r) {
            app.vue.post_download_url = r.data.download_url;
          });
      });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
