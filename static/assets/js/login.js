const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

let time = 0.5;

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
	setInterval(() => {
		time--;

		if (time < 0) {
			location.href = "/login/staff"
		}
	}, 1000);
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
