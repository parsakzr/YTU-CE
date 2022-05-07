

const loginForm = () => {
    return (
        <div className="login-form">
            <div className="login-form-header">
                <h1>Login</h1>
            </div>
            <div className="login-form-body">
                <div className="login-form-input">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" />
                </div>
                <div className="login-form-input">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" />
                </div>
                <div className="login-form-input">
                    <button id="login">Login</button>
                    <button id="register">Register</button>
                </div>
            </div>
        </div>
    );
};

export default loginForm;