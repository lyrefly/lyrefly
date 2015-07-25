module.exports = {
  context: __dirname + "/src/js",
  entry:{
	  javascript: "./main.js"
	},

  module: {
	  loaders: [
	    {
	      test: /\.js$/,
	      exclude: /node_modules/,
	      loaders: ["react-hot", "babel-loader"],
	    },
      {
        test: /\.scss$/,
        loader: "style!css!sass"
      }
	  ],
	},

  output: {
    filename: "app.js",
    path: __dirname + "/js",
  }
}
