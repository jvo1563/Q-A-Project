// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    current_user: "",
    rows: [],
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.setup_rating = (posts) => {
    // Initializes rating for post
    posts.map((post) => {
      post.rating = 0;
      post.show_likers = false;
      post.final = 0;
      post.first_load_for_like = false;
    });
  };

  app.delete_post = function (row_idx) {
    let id = app.vue.rows[row_idx].id;
    axios
      .get(delete_post_url, { params: { id: id } })
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

  app.set_rating = (row_idx, rating) => {
    let post = app.vue.rows[row_idx];
    post.rating = rating;
    axios
      .post(set_rating_url, { post_id: post.id, rating: rating })
      .then(() => {
        axios
          .get(get_likers_url, { params: { post_id: post.id } })
          .then((result) => {
            post.final = result.data.likers;
          });
      });
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    // add_post: app.add_post,
    delete_post: app.delete_post,
    set_rating: app.set_rating,
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    axios
      .get(load_posts_url)
      .then(function (response) {
        let rows = response.data.rows;
        app.enumerate(rows);
        app.setup_rating(rows);
        app.vue.current_user = response.data.current_user;
        app.vue.rows = rows;
      })
      .then(() => {
        for (let post of app.vue.rows) {
          axios
            .get(get_rating_url, { params: { post_id: post.id } })
            .then((result) => {
              post.rating = result.data.rating;
              post.final = result.data.likers;
            });
        }
      });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
