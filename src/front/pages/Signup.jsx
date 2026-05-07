import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";  // Custom hook for accessing the global state.

export const Signup = () => {
 
  const { store, dispatch } = useGlobalReducer()

  return (
    <div className="container">
      <h1>Registro</h1>


      <form>
  <div class="row mb-3">
    <label for="inputEmail3" class="col-sm-2 col-form-label">Email</label>
    <div class="col-sm-10">
      <input type="email" class="form-control" id="inputEmail3"/>
    </div>
  </div>
  <div class="row mb-3">
    <label for="inputPassword3" class="col-sm-2 col-form-label">Password</label>
    <div class="col-sm-10">
      <input type="password" class="form-control" id="inputPassword3"/>
    </div>
  </div>
  <div class="row mb-3">
    <label for="inputusername" class="col-sm-2 col-form-label">UserName</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="inputusername"/>
    </div>
  </div>
  
  
  <button type="submit" class="btn btn-primary">Sign in</button>
</form>
    </div>
  );
};
