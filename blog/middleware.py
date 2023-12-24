"""
module docstring
"""

from .models import IPAddress


class SaveIPAddressMiddleware:
    """
    class docstring
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # In this line we get the 'HTTP_X_FORWARDED_FOR' variable from nginx
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Get the first element from 'HTTP_X_FORWARDED_FOR' that is IP address
            ip = x_forwarded_for.split(',')[0]
        else:
            # Get the IP from 'REMOTE_ADDR'
            ip = request.META.get('REMOTE_ADDR')

        try:
            # See if this IP address is exists in the database
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            # If the IP address doesn't exists, then add it to the databse
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()

        # Add this IP address to the request that is send to the view
        request.user.ip_address = ip_address

        # Get the response of that request
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
