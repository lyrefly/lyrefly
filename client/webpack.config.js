module.exports = {
  context: __dirname + "/js",
  entry:{
	  javascript: "./main.js"
	},

  module: {
	  loaders: [
	    {
	      test: /\.js$/,
	      exclude: /node_modules/,
	      loaders: ["react-hot", "babel-loader"],
	    }
	  ],
	},

  output: {
    filename: "app.js",
    path: __dirname + "/dist",
  },
}