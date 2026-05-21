import React, { useEffect, useState } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	const [myImage, setMyImage] = useState(null)

	const uploadImage = async (e) => {
		console.log(e.target.files[0]);
		const formData = new FormData()

		formData.append('image', e.target.files[0])

		const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/upload",{
			method: "POST",
			body: formData,
			// header: {
			// 	"Content-Type": "multipart/formdata"
			// }
		})

		const data = await response.json()

		setMyImage(data)
		console.log(data);
		

	}
 
	return (
		<div className="text-center mt-5">
			<h1>Hello Rigo!!</h1>
			<p>
				<img src={rigoImageUrl} />
			</p>
			<div className="alert alert-info">
				{store.message || "Loading message from the backend (make sure your python backend is running)..."}
			</div>
			<p>
				This boilerplate comes with lots of documentation:{" "}
				<a href="https://start.4geeksacademy.com/starters/react-flask">
					Read documentation
				</a>
			</p>
			<img src={myImage && myImage}/>
			<input type="file" onChange={uploadImage} />
		</div>
	);
};