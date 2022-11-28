from src.auth.users.user import User
from src.constant.constants_vars import user_types_generic

class Agency(User):
	def __init__(self, provider_type, verified, firstName, lastName, email, phone_number=None, other_data=None):
		super().__init__(
			user_type=user_types_generic[2],
			provider_type=provider_type,
			verified=verified,
			firstName=firstName,
			lastName=lastName,
			email=email,
			phone_number=phone_number,
			other_data=other_data
		)