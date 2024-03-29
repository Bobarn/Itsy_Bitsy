import { useState } from "react";
import { thunkLogin } from "../../redux/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const serverResponse = await dispatch(
      thunkLogin({
        email,
        password,
      })
    );

    if (serverResponse) {
      setErrors(serverResponse);
    } else {
      navigate("/");
      closeModal();
    }
  };


  const demoLogin = async (e) => {
    e.preventDefault();
  const serverResponse = await dispatch(
    thunkLogin({
      email: "demo@aa.io",
      password: "password",
    })
  );

  if (serverResponse) {
    setErrors(serverResponse);
  } else {
    navigate("/");

    closeModal();
  }
};


  return (
    <div id='log-in-modal'>
      <h1>Log In</h1>
      <form id='log-in-form' onSubmit={handleSubmit}>
        <label className="label">
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        {errors.email && <p>{errors.email}</p>}
        <label className="label">
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {errors.password && <p>{errors.password}</p>}
        <button id="log-in-submit" type="submit">Log In</button>
      </form>
      <h5 id='demo' onClick={demoLogin}>Log in as Demo User</h5>
    </div>
  );
}

export default LoginFormModal;
