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
      post.likers = "";
      post.first_load_for_like = false;
    });
  };

  // app.add_post = function () {
  //   axios
  //     .post(add_post_url, {
  //       content: app.vue.add_content,
  //     })
  //     .then(function (response) {
  //       app.vue.rows.push({
  //         id: response.data.id,
  //         content: app.vue.add_content,
  //         name: response.data.name,
  //         user_email: response.data.user_email,
  //         rating: 0,
  //         show_likers: false,
  //         likers: "",
  //         first_load_for_like: false,
  //       });
  //       app.enumerate(app.vue.rows);
  //     });
  // };

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
    axios.post(set_rating_url, { post_id: post.id, rating: rating });
    axios
      .get(get_likers_url, { params: { post_id: post.id } })
      .then((result) => {
        post.likers = result.data.likers;
      });
  };

  app.set_liker_status = function (row_idx, new_status) {
    let post = app.vue.rows[row_idx];
    post.show_likers = new_status;
  };

  // This function will only call the controller the first time.
  // Afterwards it will just show the list of likers stored locally.
  app.get_likers = function (row_idx) {
    let post = app.vue.rows[row_idx];
    if (post.first_load_for_like === false) {
      axios
        .get(get_likers_url, { params: { post_id: post.id } })
        .then((result) => {
          post.likers = result.data.likers;
          post.first_load_for_like = true;
        });
      post.show_likers = true;
    } else {
      post.show_likers = true;
    }
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    // add_post: app.add_post,
    delete_post: app.delete_post,
    set_rating: app.set_rating,
    get_likers: app.get_likers,
    set_liker_status: app.set_liker_status,
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
              post.likers = result.data.likers;
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
